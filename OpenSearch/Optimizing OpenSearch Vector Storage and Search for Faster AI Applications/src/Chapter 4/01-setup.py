"""Chapter 4 · Steps 1-2 — enable URL model registration and create the model group.

Reference mirror of the Dev Tools steps. These scripts live directly in
``src/Chapter 4/`` (one level below ``src/``), so the import path walks up
``parents[1]`` and the shared ``.env`` is ``src/.env``.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]  # src/
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

client = open_search_client_from_env_file(_SRC / ".env")
print_opensearch_connection_test(client, raise_on_error=True)

# Step 1: allow registering model weights from a URL (persistent, safe to re-run).
client.cluster.put_settings(
    body={"persistent": {"plugins.ml_commons.allow_registering_model_via_url": True}}
)
print("Enabled: plugins.ml_commons.allow_registering_model_via_url = true")

# Step 2: create the model group; note the returned model_group_id for 02-register-model.py.
response = client.transport.perform_request(
    "POST",
    "/_plugins/_ml/model_groups/_register",
    body={"name": "huggingface-models", "description": "A group for Hugging Face transformer models"},
)
print("Model group:", response)
print("Save this model_group_id for the next script.")
