"""End-to-end "all together now" script: pipeline + index + bulk load + tune + warm.

This is the consolidated version of the seven previous scripts in this lesson,
showing how everything wires together in a single fluent flow:

    1) Create chunking + embedding ingest pipeline.
    2) Create the optimized index with k-NN + nested chunks.
    3) Disable refresh for the bulk load.
    4) Bulk-load books from sample-data.json.
    5) Force-merge + restore refresh interval + final refresh.
    6) Warm the k-NN cache.
    7) Verify shard distribution and k-NN memory stats.

In real ops you'd probably split these into separate scripts (1 + 2 in your
"infra" deploy, 3–7 in a backfill job), but seeing them in one place makes the
end-to-end shape crystal clear.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

import json
import os


client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# Use distinct names so this script doesn't clobber the index built by
# the rest of the lesson. Lets you run both flows side by side.
pipeline_id = "bookstore-chunking-pipeline-all-together"
index_name = "bookstore-rag-all-together"
embedding_model_id = os.environ.get("ML_MODEL_ID", "")

# 1) Create chunking + embedding ingest pipeline.
# Tiny token limit (25) is for demo purposes — gives you visibly many chunks
# per book so you can poke at ``content_chunks`` in the indexed docs.
pipeline_body = {
    "description": "Chunk book content for RAG embedding",
    "processors": [
        {
            "text_chunking": {
                "algorithm": {
                    "fixed_token_length": {
                        "token_limit": 25,
                        "overlap_rate": 0.2,
                        "tokenizer": "standard",
                    }
                },
                "field_map": {"content": "content_chunks"},
            }
        },
        {
            # Same Painless normalization step as 01-chunking-pipeline.py:
            # turn the flat string array into objects with chunk_index.
            "script": {
                "lang": "painless",
                "source": """
                    if (ctx.content_chunks == null) {
                        ctx.content_chunks = [];
                    } else {
                        def normalized_chunks = [];
                        for (int i = 0; i < ctx.content_chunks.size(); i++) {
                            def chunk = ctx.content_chunks.get(i);
                            if (chunk != null) {
                                normalized_chunks.add(['text': chunk, 'chunk_index': i]);
                            }
                        }
                        ctx.content_chunks = normalized_chunks;
                    }
                """,
            }
        },
        {
            "text_embedding": {
                "model_id": embedding_model_id,
                "field_map": {"content": "content_embedding"},
            }
        },
    ],
}
print("Creating/updating ingest pipeline...")
print(json.dumps(client.ingest.put_pipeline(id=pipeline_id, body=pipeline_body), indent=2))

# 2) Create index with settings + mappings (same shape as 02-bookstore-rag.py).
index_body = {
    "settings": {
        "index": {
            "knn": True,
            # Note: hard-codes the *other* pipeline name. Edit to ``pipeline_id``
            # if you want this script to be fully self-contained. The lesson
            # leaves it as-is to demonstrate that the chunking-pipeline can be
            # shared across indexes.
            "default_pipeline": "bookstore-chunking-pipeline",
            "refresh_interval": "30s",
        }
    },
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "author": {"type": "text"},
            "content": {"type": "text"},
            "content_chunks": {
                "type": "nested",
                "properties": {
                    "text": {"type": "text"},
                    "chunk_index": {"type": "integer"},
                },
            },
            "content_embedding": {
                "type": "knn_vector",
                "dimension": 768,
                "method": {
                    "engine": "faiss",
                    "name": "hnsw",
                    "parameters": {"m": 16, "ef_construction": 128},
                },
            },
            "genre": {"type": "keyword"},
            "price": {"type": "float"},
            "rating": {"type": "float"},
            "publication_year": {"type": "integer"},
            "in_stock": {"type": "boolean"},
        }
    },
}

# Re-create cleanly for predictable demo runs.
if client.indices.exists(index=index_name):
    print(f"Index '{index_name}' already exists. Deleting index.")
    client.indices.delete(index=index_name)
    print(f"Index '{index_name}' deleted successfully.")

print(json.dumps(client.indices.create(index=index_name, body=index_body), indent=2))

# 3) Disable refresh for the bulk load — major write throughput win.
client.indices.put_settings(index=index_name, body={"index": {"refresh_interval": "-1"}})

# 4) Bulk-load data from src/sample-data.json.
sample_data_path = Path(__file__).resolve().parents[2] / "sample-data.json"
with open(sample_data_path, encoding="utf-8") as f:
    books = json.load(f).get("results", [])

actions = []
for book in books:
    summaries = book.get("summaries") or []
    passage_text = summaries[0] if summaries else ""
    doc = {
        "id": str(book.get("id", "")),
        "title": book.get("title", ""),
        "authors": book.get("authors", []),
        "subjects": book.get("subjects", []),
        "content": passage_text,
        "bookshelves": book.get("bookshelves", []),
    }
    actions.append({"index": {"_index": index_name, "_id": doc["id"]}})
    actions.append(doc)

bulk_response = client.bulk(body=actions, request_timeout=600)
failed = [item for item in bulk_response.get("items", []) if "error" in item.get("index", {})]
print(f"Bulk ingest complete: {len(books) - len(failed)} succeeded, {len(failed)} failed")

# 5) Optimize: force-merge to fewer segments, then restore refresh, then refresh once.
client.indices.forcemerge(index=index_name, max_num_segments=5)
client.indices.put_settings(index=index_name, body={"index": {"refresh_interval": "1s"}})
client.indices.refresh(index=index_name)

# 6) Warm k-NN cache so the first user query is already fast.
warmup_response = client.transport.perform_request("GET", f"/_plugins/_knn/warmup/{index_name}")
print("Warmup response:")
print(json.dumps(warmup_response, indent=2))

# 7) Final verification: shard layout + k-NN memory stats.
shards = client.cat.shards(
    index=index_name,
    params={"v": "true", "h": "index,shard,prirep,state,docs,store"},
    format="json",
)
print("Shard overview:")
print(json.dumps(shards, indent=2))

knn_stats = client.transport.perform_request("GET", "/_plugins/_knn/stats")
# Per-node stats — pick the first one as a sample (works fine in single-node labs).
nodes_stats = knn_stats.get("nodes", {})
first_node_stats = next(iter(nodes_stats.values()), {})
graph_memory_usage_percentage = first_node_stats.get("graph_memory_usage_percentage", "N/A")
cache_hit_rate = first_node_stats.get("cache_hit_rate", "N/A")
graph_query_requests = first_node_stats.get("graph_query_requests", "N/A")
print(f"graph_memory_usage_percentage: {graph_memory_usage_percentage}")
print(f"cache_hit_rate: {cache_hit_rate}")
print(f"graph_query_requests: {graph_query_requests}")
