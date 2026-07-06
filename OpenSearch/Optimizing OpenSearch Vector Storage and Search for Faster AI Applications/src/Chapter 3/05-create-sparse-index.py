"""Create my-sparse-neural-index for chunked neural sparse search.

Key design choices:
    * ``default_pipeline`` attaches ``nlp-ingest-pipeline`` (created in
      ``04-sparse-ingest-pipeline.py``) so every document is chunked +
      sparse-encoded automatically at index time.
    * ``passage_text`` holds the full document text (BM25 target).
    * ``passage_chunk`` is filled by the chunking processor.
    * ``passage_embedding`` is a **nested** field, one entry per chunk, each
      with a ``rank_features`` map (token -> weight). A ``neural_sparse`` query
      can score chunks independently and aggregate with ``score_mode``.

Why ``rank_features`` instead of ``sparse_vector``? The sparse-encoding model
emits subword **string** keys; ``sparse_vector`` only accepts numeric keys and
indexing fails with ``[sparse_vector] fields should be valid integer``.
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

index_name = "my-sparse-neural-index"
# Clean slate: deleting first lets us iterate on the mapping.
if client.indices.exists(index=index_name):
    client.indices.delete(index=index_name)
    print(f"Deleted existing index: {index_name}")

client.indices.create(
    index=index_name,
    body={
        "settings": {
            "index": {
                "number_of_shards": 2,
                "number_of_replicas": 1,
                # Every doc runs through chunking + sparse encoding on ingest.
                "default_pipeline": "nlp-ingest-pipeline",
            }
        },
        "mappings": {
            "properties": {
                "passage_text": {"type": "text"},
                "passage_chunk": {"type": "text"},
                "passage_embedding": {
                    # ``nested`` keeps chunk sub-documents independently queryable.
                    "type": "nested",
                    "properties": {
                        "sparse_encoding": {"type": "rank_features"},
                    },
                },
            }
        },
    },
)
print(f"Created index: {index_name} (default_pipeline = nlp-ingest-pipeline)")
