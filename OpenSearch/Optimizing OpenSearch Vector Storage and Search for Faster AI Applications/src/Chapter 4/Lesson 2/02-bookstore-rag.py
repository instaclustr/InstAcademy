"""Create the production-shaped ``bookstore-rag`` index used by the rest of this lesson.

Highlights vs the unoptimized index in ``00-set-up-books-unoptimized.py``:
    * ``index.knn: true`` and a ``knn_vector`` field for content embedding.
    * Default pipeline = the chunking pipeline from ``01-chunking-pipeline.py``
      so docs are auto-chunked and auto-embedded.
    * ``refresh_interval: 30s`` — slower refresh saves indexing CPU. Default is
      1s; bumping to 30s is the simplest write-throughput optimization.
    * ``nested`` mapping on ``content_chunks`` so each chunk is independently
      queryable (good for RAG, where you want to retrieve specific snippets).
    * ``keyword`` types for ``genre`` (vs ``text`` in the unoptimized version)
      so faceting/filtering on genre is exact.
"""

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

index_name = "bookstore-rag"
index_body = {
    "settings": {
        "index": {
            # k-NN plugin enabled for this index — needed for ``knn_vector`` queries.
            "knn": True,
            # Auto-attach the chunking + embedding pipeline.
            "default_pipeline": "bookstore-chunking-pipeline",
            # Refresh every 30s instead of 1s — fewer Lucene refresh cycles,
            # more efficient indexing, at the cost of "30s before new docs
            # become searchable". For a RAG/bookstore index that's fine.
            "refresh_interval": "30s",
        }
    },
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "author": {"type": "text"},
            "content": {"type": "text"},
            "content_chunks": {
                # ``nested`` keeps each chunk as an independently-queryable
                # subdocument. Without ``nested`` the array elements get
                # flattened and you lose per-chunk grouping.
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
                    # ``faiss`` engine = Facebook AI Similarity Search. Faster
                    # than Lucene at very large scale and supports quantization,
                    # but requires off-heap memory budgeting.
                    "engine": "faiss",
                    "name": "hnsw",
                    # ``m`` (links per node) and ``ef_construction`` (search
                    # width during graph build) trade index-time work for
                    # query-time recall. m=16/efc=128 is a balanced default.
                    "parameters": {"m": 16, "ef_construction": 128},
                },
            },
            # ``keyword`` for exact-match facets/filters (vs ``text`` which
            # would tokenize "Science Fiction" into two terms).
            "genre": {"type": "keyword"},
            "price": {"type": "float"},
            "rating": {"type": "float"},
            "publication_year": {"type": "integer"},
            "in_stock": {"type": "boolean"},
        }
    },
}

# Recreate the index on every run so mapping changes take effect.
# OpenSearch mappings are mostly immutable — you can add fields but not change
# existing types. Re-create is the only way to iterate cleanly during a lab.
if client.indices.exists(index=index_name):
    print(f"Index '{index_name}' already exists. Deleting index.")
    client.indices.delete(index=index_name)
    print(f"Index '{index_name}' deleted successfully.")

response = client.indices.create(index=index_name, body=index_body)
print(json.dumps(response, indent=2))
print(f"Index '{index_name}' created successfully.")
