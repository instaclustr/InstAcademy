"""Lesson 2-2 Step 8: create the k-NN vector index with the pipeline attached.

This index pairs with the pipeline from ``05-create-index-pipeline.py``:
    * Documents are indexed with plain ``passage_text``.
    * The pipeline turns that into a 768-dim ``passage_embedding`` automatically.
    * The mapping declares ``passage_embedding`` as a ``knn_vector`` so it can be
      queried with ``neural`` / ``knn`` queries later.

``dimension: 768`` matches msmarco-distilbert-base-tas-b. Swap models and you must
change this, or indexing fails with a dimension-mismatch error.
"""

import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"

client = open_search_client_from_env_file(_ENV_FILE)
print_opensearch_connection_test(client, raise_on_error=True)

index_name = "vector-search-index"
client.indices.create(
    index=index_name,
    body={
        "settings": {
            # Required for knn_vector fields to be queryable.
            "index.knn": True,
            # Route every indexing request through the embeddings pipeline.
            "default_pipeline": "vector-search-embeddings-pipeline",
        },
        "mappings": {
            "properties": {
                "id": {"type": "text"},
                "title": {"type": "text"},
                # Nested author objects aren't searched — store without indexing.
                "authors": {"type": "object", "enabled": False},
                "subjects": {"type": "keyword"},
                "bookshelves": {"type": "keyword"},
                "passage_text": {"type": "text"},
                "passage_embedding": {
                    "type": "knn_vector",
                    "dimension": 768,
                    "method": {
                        # Lucene HNSW: pure-Java, easy to operate, good baseline.
                        "engine": "lucene",
                        # L2 (Euclidean); works well for length-normalized vectors.
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
