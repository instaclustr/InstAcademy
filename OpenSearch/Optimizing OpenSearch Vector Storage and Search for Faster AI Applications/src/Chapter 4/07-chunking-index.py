"""Chapter 4 · Steps 14-17 — unoptimized baseline, chunking pipeline, bookstore-rag, fast bulk.

Rebuilds the index the production way: native text_chunking, nested chunks, FAISS HNSW,
and the fast-bulk recipe (refresh off -> bulk -> force-merge -> refresh on).
"""

import os
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_REPO = _SRC.parent
client = open_search_client_from_env_file(_SRC / ".env")
print_opensearch_connection_test(client, raise_on_error=True)

model_id = os.getenv("ML_MODEL_ID")
if not model_id:
    sys.exit("Set ML_MODEL_ID in src/.env before running this script.")

# Step 14: unoptimized baseline (intentionally wrong field types, no vector).
if not client.indices.exists(index="books-unoptimized"):
    client.indices.create(index="books-unoptimized", body={
        "settings": {"index": {"number_of_shards": 2, "number_of_replicas": 1}},
        "mappings": {"properties": {
            "book_id": {"type": "text"}, "title": {"type": "text"}, "author": {"type": "text"},
            "isbn": {"type": "text"}, "genre": {"type": "text"}, "published_year": {"type": "integer"},
            "price": {"type": "float"}, "rating": {"type": "integer"}, "content": {"type": "text"},
        }},
    })
    print("Created books-unoptimized")
print("Baseline mapping:", client.indices.get_mapping(index="books-unoptimized"))

# Step 15: chunking + normalize + embed pipeline.
client.ingest.put_pipeline(id="bookstore-chunking-pipeline", body={
    "description": "Chunk and embed book content for RAG",
    "processors": [
        {"text_chunking": {
            "algorithm": {"fixed_token_length": {"token_limit": 384, "overlap_rate": 0.2, "tokenizer": "standard"}},
            "field_map": {"content": "content_chunks"},
        }},
        {"script": {"lang": "painless", "source":
            "if (ctx.content_chunks == null) { ctx.content_chunks = []; } else { def n = []; "
            "for (int i = 0; i < ctx.content_chunks.size(); i++) { def c = ctx.content_chunks.get(i); "
            "if (c != null) { n.add(['text': c, 'chunk_index': i]); } } ctx.content_chunks = n; }"}},
        {"text_embedding": {"model_id": model_id, "field_map": {"content": "content_embedding"}}},
    ],
})
print("Created bookstore-chunking-pipeline")

# Step 16: optimized index.
if client.indices.exists(index="bookstore-rag"):
    client.indices.delete(index="bookstore-rag")
client.indices.create(index="bookstore-rag", body={
    "settings": {"index": {"knn": True, "default_pipeline": "bookstore-chunking-pipeline", "refresh_interval": "30s"}},
    "mappings": {"properties": {
        "book_id": {"type": "keyword"}, "title": {"type": "text"}, "author": {"type": "text"},
        "content": {"type": "text"},
        "content_chunks": {"type": "nested", "properties": {"text": {"type": "text"}, "chunk_index": {"type": "integer"}}},
        "content_embedding": {"type": "knn_vector", "dimension": 768, "method": {
            "engine": "faiss", "name": "hnsw", "space_type": "l2", "parameters": {"m": 16, "ef_construction": 128}}},
        "genre": {"type": "keyword"}, "price": {"type": "float"}, "rating": {"type": "float"},
        "publication_year": {"type": "integer"}, "in_stock": {"type": "boolean"},
    }},
})
print("Created bookstore-rag")

# Step 17: fast bulk recipe.
client.indices.put_settings(index="bookstore-rag", body={"index": {"refresh_interval": "-1"}})
body = (_REPO / "rest" / "bulk" / "chapter-4-bookstore-rag.ndjson").read_text()
resp = client.bulk(body=body, request_timeout=600)
errors = [i for i in resp.get("items", []) if i.get("index", {}).get("error")]
print(f"Bulk load: {len(errors)} failed")
client.indices.forcemerge(index="bookstore-rag", max_num_segments=5)
client.indices.put_settings(index="bookstore-rag", body={"index": {"refresh_interval": "1s"}})
client.indices.refresh(index="bookstore-rag")
print("Force-merged, restored refresh, refreshed.")
