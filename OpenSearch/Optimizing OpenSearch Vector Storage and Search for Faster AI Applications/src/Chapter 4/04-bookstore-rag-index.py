"""Chapter 4 · Steps 5-7 — RAG ingest pipeline + bookstore-rag-index (FAISS HNSW) + bulk load.

Reads ML_MODEL_ID from src/.env. Bulk body comes from the enriched course file
rest/bulk/chapter-4-bookstore-rag-index.ndjson (title/author/content + genre/price/
rating/publication_year/in_stock). Each document is embedded server-side, so allow
several minutes on a trial cluster.
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
    sys.exit("Set ML_MODEL_ID in src/.env (Step 4) before running this script.")

# Step 5: ingest pipeline — embed content -> content_embedding.
client.ingest.put_pipeline(
    id="bookstore-rag-ingest-pipeline",
    body={
        "description": "Embed book content for RAG retrieval",
        "processors": [{"text_embedding": {"model_id": model_id, "field_map": {"content": "content_embedding"}}}],
    },
)
print("Created ingest pipeline: bookstore-rag-ingest-pipeline")

# Step 6: FAISS HNSW index with typed metadata fields.
index_name = "bookstore-rag-index"
if client.indices.exists(index=index_name):
    print(f"Index {index_name} already exists; skipping create.")
else:
    client.indices.create(
        index=index_name,
        body={
            "settings": {
                "index": {"knn": True, "number_of_shards": 2, "number_of_replicas": 1},
                "default_pipeline": "bookstore-rag-ingest-pipeline",
            },
            "mappings": {
                "properties": {
                    "book_id": {"type": "keyword"},
                    "title": {"type": "text"},
                    "author": {"type": "text"},
                    "content": {"type": "text"},
                    "genre": {"type": "keyword"},
                    "price": {"type": "float"},
                    "rating": {"type": "float"},
                    "publication_year": {"type": "integer"},
                    "in_stock": {"type": "boolean"},
                    "content_embedding": {
                        "type": "knn_vector",
                        "dimension": 768,
                        "method": {
                            "engine": "faiss",
                            "name": "hnsw",
                            "space_type": "l2",
                            "parameters": {"m": 16, "ef_construction": 128},
                        },
                    },
                }
            },
        },
    )
    print(f"Created index: {index_name}")

# Step 7: bulk load from the enriched course file (raw ndjson body).
bulk_file = _REPO / "rest" / "bulk" / "chapter-4-bookstore-rag-index.ndjson"
body = bulk_file.read_text()
response = client.bulk(body=body, request_timeout=600)
errors = [i for i in response.get("items", []) if i.get("index", {}).get("error")]
print(f"Bulk load: {'errors' if errors else 'no errors'} ({len(errors)} failed)")
client.indices.refresh(index=index_name)
print(f"Refreshed {index_name}")
