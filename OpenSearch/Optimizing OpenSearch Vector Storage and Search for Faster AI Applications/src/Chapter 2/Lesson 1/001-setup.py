"""Enable URL model registration and create a model group for ML Commons.

What this script teaches:
    * The cluster-wide setting that lets ML Commons download model artifacts
      from external URLs (e.g. Hugging Face). It's off by default for safety.
    * Model **groups** — a permissions/organisation primitive in ML Commons.
      Every registered model belongs to a group, so you create the group first
      and feed its id into the model registration request in the next script.

Run this once per cluster (the setting is persistent), then take note of the
``model_group_id`` printed at the bottom — script ``002`` consumes it.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client)

# Allow registering models via URL (e.g. Hugging Face distilbert for ML Commons).
# ``persistent`` settings survive cluster restarts; ``transient`` ones do not.
# By default the cluster refuses to fetch arbitrary URLs — turning this on lets
# the next script point at a Hugging Face model and download it on demand.
client.cluster.put_settings(
    body={
        "persistent": {
            "plugins.ml_commons.allow_registering_model_via_url": True,
        }
    }
)
print("Cluster settings updated: allow_registering_model_via_url = true")

# Create a model group to organize uploaded models.
# ML Commons attaches an access policy at the group level (public/private/
# restricted), so you typically have one group per use case or team.
# The response includes ``model_group_id`` — copy it into the argv of 002-register-model.py.
response = client.transport.perform_request(
    "POST",
    "/_plugins/_ml/model_groups/_register",
    body={
        "name": "huggingface-models",
        "description": "A group for Hugging Face transformer models",
    },
)
print("Model group registration response:", response)
