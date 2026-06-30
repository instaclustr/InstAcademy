"""Create bookstore-rag-index for RAG: book metadata, text chunks, and k-NN passage_embedding.

This is a one-shot setup script:
    1. Creates an ingest pipeline that auto-embeds ``passage_text``.
    2. Creates the target index (with k-NN enabled, default pipeline attached).
    3. Bulk-loads books from ``src/sample-data.json``.

Why combine all three steps?
    For a RAG (Retrieval-Augmented Generation) workflow you usually want the
    pipeline + index + data wired up together. Splitting into separate scripts
    is great for teaching; folding them together is how you'd actually script
    a real environment setup.
"""

import os
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

import json


client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# Step 1: PUT /_ingest/pipeline/bookstore-rag-ingest-pipeline
# Same "text_embedding" processor we saw in Chapter 2 — reads ``passage_text``,
# writes a 768-dim ``passage_embedding`` using the deployed model.
pipeline_id = "bookstore-rag-ingest-pipeline"
response = client.ingest.put_pipeline(
    id=pipeline_id,
    body={
        "description": "Pipeline for processing OpenSearch index data",
        "processors": [
            {
                "text_embedding": {
                    "model_id": os.getenv("ML_MODEL_ID"),
                    "field_map": {
                        "passage_text": "passage_embedding"
                    }
                }
            }
        ],
    },
)

if response.get("acknowledged"):
    print(f"Created ingest pipeline: {pipeline_id}")
else:
    print("Pipeline response:", response)

# Step 2: index settings — k-NN enabled, sharded, attached to the pipeline.
_index_settings = {
    # Required for ``knn_vector`` fields to be queryable.
    "index.knn": True,
    "index": {
        # 2 shards splits the load — modest but enough to demo distributed search.
        "number_of_shards": 2,
        # 1 replica = each shard exists twice for HA. Set 0 for single-node labs.
        "number_of_replicas": 1,
    },
}
if pipeline_id:
    # Every indexing call into this index goes through the pipeline unless
    # the caller passes ``?pipeline=...`` explicitly.
    _index_settings["default_pipeline"] = pipeline_id

# PUT /bookstore-rag-index
index_name = "bookstore-rag-index"
if client.indices.exists(index=index_name):
    # Don't drop existing data — assume the lab user wants idempotent re-runs.
    print(f"Index {index_name} already exists; skipping create.")
else:
    client.indices.create(
        index=index_name,
        body={
            "settings": _index_settings,
            "mappings": {
                "properties": {
                    "book_id": {"type": "keyword"},
                    "title": {"type": "text"},
                    "author": {"type": "text"},
                    "isbn": {"type": "keyword"},
                    "genre": {"type": "keyword"},
                    "published_year": {"type": "integer"},
                    "chunk_index": {"type": "integer"},
                    "passage_text": {"type": "text"},
                    "passage_embedding": {
                        "type": "knn_vector",
                        # Matches the all-mpnet-base-v2 output dim.
                        "dimension": 768,
                        "method": {
                            # ``lucene`` HNSW — easy mode, ships with Lucene.
                            "engine": "lucene",
                            "space_type": "l2",
                            "name": "hnsw",
                            "parameters": {},
                        },
                    },
                }
            },
        },
    )
    print(f"Created index: {index_name}")
    if pipeline_id:
        print(f"Default ingest pipeline: {pipeline_id}")
    else:
        print(
            "No BOOKSTORE_RAG_PIPELINE_ID set; index documents with precomputed "
            "passage_embedding or attach a text_embedding pipeline later."
        )

# Step 3: load sample-data.json from src/.
script_dir = Path(__file__).resolve().parents[2]
sample_data_path = script_dir / "sample-data.json"
with open(sample_data_path, encoding="utf-8") as f:
    data = json.load(f)
books = data.get("results", [])
index_name = "bookstore-rag-index"

def doc_for_book(book):
    """Project a Gutendex record to the shape this index expects."""
    summaries = book.get("summaries") or []
    passage_text = summaries[0] if summaries else ""
    return {
        "id": str(book.get("id", "")),
        "title": book.get("title", ""),
        "authors": book.get("authors", []),
        "subjects": book.get("subjects", []),
        "passage_text": passage_text,
        "bookshelves": book.get("bookshelves", []),
    }

actions = []
for book in books:
    doc = doc_for_book(book)
    actions.append({"index": {"_index": index_name, "_id": doc["id"]}})
    actions.append(doc)

# Long timeout because each doc triggers a model inference at index time.
response = client.bulk(body=actions, request_timeout=600)
failed = [
    item
    for item in response.get("items", [])
    if "error" in item.get("index", item.get("index", {}))
]
num_failed = len(failed)
num_ok = len(books) - num_failed
if num_failed:
    print(f"Bulk ingest: {num_ok} succeeded, {num_failed} failed")
    for item in failed[:5]:
        print("  ", item.get("index", item))
    if num_failed > 5:
        print(f"  ... and {num_failed - 5} more")
else:
    print(f"Ingested {len(books)} books into {index_name}")
