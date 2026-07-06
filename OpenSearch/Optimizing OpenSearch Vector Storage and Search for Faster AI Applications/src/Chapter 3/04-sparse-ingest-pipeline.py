"""Create an ingest pipeline that chunks text then sparse-encodes each chunk.

Pipeline flow (top to bottom):
    1. ``text_chunking``: split ``passage_text`` into fixed-length token chunks,
       written into ``passage_chunk`` (an array of strings).
    2. ``sparse_encoding``: for each chunk, call the deployed sparse model and
       emit a nested object with ``sparse_encoding`` (token -> weight) under
       ``passage_embedding``.

Create this **before** the index (``05-create-sparse-index.py``) so the index
can reference it as ``default_pipeline``.

Why chunking? Encoders have a max sequence length; long passages get truncated
unless split. Chunking also improves precision — a short relevant passage
scores better than a long doc that's only partly relevant.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"
load_dotenv(_ENV_FILE)

# Fail fast if the sparse model hasn't been deployed/configured yet.
if not (os.environ.get("ML_MODEL_ID") or "").strip():
    print("Set ML_MODEL_ID in src/.env (deployed sparse encoding model).", file=sys.stderr)
    sys.exit(1)

client = open_search_client_from_env_file(_ENV_FILE)

print_opensearch_connection_test(client, raise_on_error=True)

pipeline_id = "nlp-ingest-pipeline"
response = client.ingest.put_pipeline(
    id=pipeline_id,
    body={
        "description": "A sparse encoding ingest pipeline",
        "processors": [
            {
                "text_chunking": {
                    "algorithm": {
                        # ``fixed_token_length`` chunks by token count.
                        "fixed_token_length": {
                            # 5 tokens per chunk is unusually small — kept low
                            # so you can clearly see per-chunk output. Real apps
                            # use 128–512.
                            "token_limit": 5,
                            # 50% overlap so phrases spanning a boundary are
                            # encoded together at least once.
                            "overlap_rate": 0.5,
                            "tokenizer": "standard",
                        }
                    },
                    "field_map": {
                        "passage_text": "passage_chunk",
                    },
                },
            },
            {
                "sparse_encoding": {
                    "model_id": os.environ.get("ML_MODEL_ID"),
                    # ``prune_type`` + ``prune_ratio`` discard low-weight tokens
                    # to keep vectors small. ``max_ratio`` 0.1 keeps only weights
                    # >= 10% of the max weight in that vector.
                    "prune_type": "max_ratio",
                    "prune_ratio": 0.1,
                    "field_map": {
                        "passage_chunk": "passage_embedding",
                    },
                }
            },
        ],
    },
)

if response.get("acknowledged"):
    print(f"Created ingest pipeline: {pipeline_id}")
    print("Next: python 05-create-sparse-index.py")
else:
    print("Response:", response)
