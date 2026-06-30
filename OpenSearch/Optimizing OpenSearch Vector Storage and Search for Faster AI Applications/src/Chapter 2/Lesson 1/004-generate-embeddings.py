"""Run text-embedding inference against a deployed model (ML Commons predict API).

This is the payoff of Lesson 1: prove the model is actually running by
asking it to embed a couple of strings. The cluster turns each string into a
fixed-length dense vector (e.g. 768 floats for distilbert-tas-b).

In later lessons you won't call ``_predict`` directly — instead you'll wire the
same model id into an **ingest pipeline** so embeddings are generated
automatically whenever a document is indexed.
"""

import json
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client)

if len(sys.argv) < 2:
    print("Usage: python 004-generate-embeddings.py <model_id>", file=sys.stderr)
    sys.exit(1)

model_id = sys.argv[1]

# Text embedding models use this route (not .../models/{id}/_predict). See:
# https://github.com/opensearch-project/ml-commons/blob/main/docs/model_serving_framework/text_embedding_model_examples.md
#
# Why the special route? ML Commons dispatches by **algorithm**, so embedding
# models use ``/_predict/text_embedding/{id}`` and remote LLMs use a different
# route. Mixing them up gives a 400.
#
# Body fields:
#   text_docs: list of strings to embed
#   return_number: include the actual numeric vector in the response
#   target_response: what kind of output to return; ``sentence_embedding`` for
#                   pooled per-sentence vectors (vs. token-level)
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
# ``default=str`` lets json.dumps fall back to str() for types it doesn't
# natively understand (e.g. numpy floats) — handy when poking around with
# different response shapes.
print(json.dumps(response, indent=2, default=str))
