"""Enable URL model registration and create a model group (Chapter 3 version).

Identical to Chapter 2's setup script — Chapter 3 introduces neural **sparse**
search, which uses a different model architecture. We still need:
    1. The cluster setting that allows fetching model weights from a URL.
    2. A model group to attach the new model to.

Run this once, then feed the printed ``model_group_id`` into ``001a-register-model.py``.
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

# Allow registering models via URL (e.g. Hugging Face distilbert for ML Commons).
# This is idempotent — already-true clusters just re-acknowledge.
client.cluster.put_settings(
    body={
        "persistent": {
            "plugins.ml_commons.allow_registering_model_via_url": True,
        }
    }
)
print("Cluster settings updated: allow_registering_model_via_url = true")

# POST /_plugins/_ml/model_groups/_register
# Re-creating a group with the same name will fail; either reuse the existing
# group or pick a new name. The cluster returns the new group's id in the
# response — note it for the next script.
response = client.transport.perform_request(
    "POST",
    "/_plugins/_ml/model_groups/_register",
    body={
        "name": "huggingface-models",
        "description": "A group for Hugging Face transformer models",
    },
)
print("Model group registration response:", response)
