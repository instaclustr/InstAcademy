"""Create a k-NN vector search index with an attached ingest pipeline.

This index pairs with the pipeline from ``001-create-index-pipeline.py``:
    * Documents are indexed with plain ``passage_text``.
    * The pipeline turns that into a 768-dim ``passage_embedding`` automatically.
    * The mapping declares ``passage_embedding`` as a ``knn_vector`` so it can
      be queried with the ``neural`` / ``knn`` query types later.

Dimension 768 matches the output size of the msmarco-distilbert-base-tas-b
model from Lesson 1. If you swap models you also have to change ``dimension``
here, otherwise indexing will fail with a dimension-mismatch error.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

# Configure your OpenSearch connection.
client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# PUT /vector-search-index
index_name = "vector-search-index"
client.indices.create(
    index=index_name,
    body={
        "settings": {
            # Required for ``knn_vector`` fields to be queryable with ``knn`` queries.
            "index.knn": True,
            # ``default_pipeline`` makes every indexing request go through the
            # named pipeline unless the client passes ``?pipeline=...`` to
            # override. This is how automatic embedding generation works.
            "default_pipeline": "vector-search-embeddings-pipeline",
        },
        "mappings": {
            "properties": {
                "id": {"type": "text"},
                "passage_embedding": {
                    "type": "knn_vector",
                    # 768 == output dim of the deployed sentence-transformer.
                    "dimension": 768,
                    "method": {
                        # ``lucene`` engine = pure-Java HNSW implementation
                        # bundled with Lucene. Easy to operate, good baseline
                        # performance for moderate-scale workloads.
                        "engine": "lucene",
                        # L2 (Euclidean) distance. Pick the metric your
                        # embedding model was trained for; sentence transformers
                        # are typically trained for cosine, but L2 works well
                        # if vectors are length-normalized.
                        "space_type": "l2",
                        "name": "hnsw",
                        "parameters": {},
                    },
                },
                "passage_text": {"type": "text"},
            }
        },
    },
)
print(f"Created index: {index_name}")
