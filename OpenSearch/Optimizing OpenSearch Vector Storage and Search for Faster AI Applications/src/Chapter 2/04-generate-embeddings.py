"""Lesson 2-1 Step 6 / Lesson 2-3 Step 14: dense text-embedding inference.

The payoff of Lesson 2-1: prove the model runs by asking it to embed a couple of
strings. Each string becomes a fixed-length **dense** vector (768 floats for
msmarco-distilbert-base-tas-b) where every position is populated — contrast this
with the sparse token->weight map shown in Lesson 2-3.

In later lessons you won't call ``_predict`` directly — you wire the same model
id into an ingest pipeline so embeddings are generated automatically at index time.
"""

import json
import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"

client = open_search_client_from_env_file(_ENV_FILE)

print_opensearch_connection_test(client)

if len(sys.argv) < 2:
    print("Usage: python 04-generate-embeddings.py <model_id>", file=sys.stderr)
    sys.exit(1)

model_id = sys.argv[1]

# Text embedding models dispatch on algorithm, so they use
# /_predict/text_embedding/{id} (not .../models/{id}/_predict). Body fields:
#   text_docs: list of strings to embed
#   return_number: include the numeric vector in the response
#   target_response: ``sentence_embedding`` = pooled per-sentence vectors
response = client.transport.perform_request(
    "POST",
    f"/_plugins/_ml/_predict/text_embedding/{model_id}",
    body={
        "text_docs": ["Some example text to embed.", "Another sentence for testing."],
        "return_number": True,
        "target_response": ["sentence_embedding"],
    },
)
print("Embedding generation response:")
print(json.dumps(response, indent=2, default=str))
