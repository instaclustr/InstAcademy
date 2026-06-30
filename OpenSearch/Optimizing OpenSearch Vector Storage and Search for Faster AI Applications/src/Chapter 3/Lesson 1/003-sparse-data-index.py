"""Create my-sparse-neural-index for chunked neural sparse search.

Key concepts in this index design:
    * ``passage_text`` holds the full document text (no chunking).
    * ``passage_chunk`` is filled by the ingest pipeline (text_chunking).
    * ``passage_embedding`` is a **nested** field holding one entry per chunk,
      each containing a ``rank_features`` map (token -> weight). The cluster
      can run a ``neural_sparse`` query on the inner ``sparse_encoding`` field
      and score chunks independently before aggregating with ``score_mode``.

Why ``rank_features`` instead of ``sparse_vector``?
    ``text_chunking`` + ``sparse_encoding`` writes **nested** objects under
    ``passage_embedding``, each with a ``sparse_encoding`` map (token string ->
    weight). That shape matches ``rank_features`` (see OpenSearch text-chunking
    + sparse docs).

    Do **not** map ``sparse_encoding`` as ``sparse_vector`` for this model:
    ``sparse_vector`` only accepts numeric string keys (for example token id
    ``1000`` as the map key), while the sparse-encoding model emits subword
    strings; indexing then fails with::

        [sparse_vector] fields should be valid integer
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

index_name = "my-sparse-neural-index"
# Clean slate: deleting first lets us iterate on the mapping without restart.
if client.indices.exists(index=index_name):
    client.indices.delete(index=index_name)
    print(f"Deleted existing index: {index_name}")

client.indices.create(
    index=index_name,
    body={
        # Multiple shards (2) + a replica gives a slightly more realistic
        # operational shape than the single-shard demo in Chapter 1.
        "settings": {
            "index": {
                "number_of_shards": 2,
                "number_of_replicas": 1,
            }
        },
        "mappings": {
            "properties": {
                "passage_text": {"type": "text"},
                "passage_chunk": {"type": "text"},
                "passage_embedding": {
                    # ``nested`` keeps the inner objects (chunk + encoding) as
                    # independently-queryable subdocuments. Without ``nested``,
                    # OpenSearch flattens arrays and you lose the per-chunk grouping.
                    "type": "nested",
                    "properties": {
                        # ``rank_features`` stores a map of feature_name->weight
                        # and supports query types like ``rank_feature`` and
                        # ``neural_sparse`` for sparse-vector retrieval.
                        "sparse_encoding": {"type": "rank_features"},
                    },
                },
            }
        },
    },
)
print(f"Created index: {index_name}")
