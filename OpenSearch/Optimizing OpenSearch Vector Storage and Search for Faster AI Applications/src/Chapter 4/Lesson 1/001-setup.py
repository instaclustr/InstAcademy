"""Enable URL model registration and create a model group (Chapter 4 version).

Identical pattern to Chapter 2 / Chapter 3 setup scripts — every chapter that
introduces a new ML model needs:
    1. The cluster setting that allows fetching weights from a URL.
    2. A model group to attach the new model to.

In Chapter 4 the model is ``all-mpnet-base-v2`` (a stronger dense sentence
transformer than Chapter 2's distilbert), used for the "bookstore RAG" demo.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client)

# Persistent cluster setting — safe to re-run, already-true is a no-op.
client.cluster.put_settings(
    body={
        "persistent": {
            "plugins.ml_commons.allow_registering_model_via_url": True,
        }
    }
)
print("Cluster settings updated: allow_registering_model_via_url = true")

# Create a model group; note the returned ``model_group_id`` for 002-register-model.py.
response = client.transport.perform_request(
    "POST",
    "/_plugins/_ml/model_groups/_register",
    body={
        "name": "huggingface-models",
        "description": "A group for Hugging Face transformer models",
    },
)
print("Model group registration response:", response)
