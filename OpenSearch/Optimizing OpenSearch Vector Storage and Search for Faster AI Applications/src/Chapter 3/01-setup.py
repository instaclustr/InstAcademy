"""Enable URL model registration and create a model group (Chapter 3, sparse).

Chapter 3 introduces neural **sparse** search, which uses a different model
architecture than Chapter 2's dense encoder. Setup is the same two pieces:
    1. The cluster setting that allows fetching model weights from a URL.
    2. A model group to attach the new model to.

Run this once, then feed the printed ``model_group_id`` into ``02-register-model.py``.
"""

import sys
from pathlib import Path

# Scripts live at src/Chapter 3/*.py, so ``src/`` is one level up (parents[1]).
_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"

client = open_search_client_from_env_file(_ENV_FILE)

print_opensearch_connection_test(client)

# Allow registering models via URL (ML Commons blocks this by default).
# Idempotent — an already-true cluster just re-acknowledges.
client.cluster.put_settings(
    body={
        "persistent": {
            "plugins.ml_commons.allow_registering_model_via_url": True,
        }
    }
)
print("Cluster settings updated: allow_registering_model_via_url = true")

# POST /_plugins/_ml/model_groups/_register
# Reuse the Chapter 2 "huggingface-models" group if it exists; re-creating a
# group with the same name fails. The response carries the new group's id.
response = client.transport.perform_request(
    "POST",
    "/_plugins/_ml/model_groups/_register",
    body={
        "name": "huggingface-models",
        "description": "A group for Hugging Face transformer models",
    },
)
print("Model group registration response:", response)
