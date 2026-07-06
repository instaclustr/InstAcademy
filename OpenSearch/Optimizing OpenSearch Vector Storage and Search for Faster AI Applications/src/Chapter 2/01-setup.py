"""Lesson 2-1 Steps 2-3: enable ML Commons settings and create a model group.

What this script teaches:
    * The cluster-wide ML Commons settings that make model registration and
      deployment reliable on a small managed cluster (no dedicated ML node).
    * Model **groups** — the organization/access-control primitive in ML Commons.
      Every registered model belongs to a group, so you create the group first
      and feed its id into the model registration request in ``02``.

Run this once per cluster (the settings are persistent), then note the
``model_group_id`` printed at the bottom — script ``02`` consumes it.
"""

import sys
from pathlib import Path

# These scripts live at ``src/Chapter 2/*.py``. ``parents[1]`` is ``src/`` — the
# folder that holds ``utils/`` and the shared ``.env``.
_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"

client = open_search_client_from_env_file(_ENV_FILE)

print_opensearch_connection_test(client)

# Enable the ML Commons settings the workshop relies on. ``persistent`` settings
# survive cluster restarts; ``transient`` ones do not.
#   * allow_registering_model_via_url  -> needed for custom model_url registration
#   * only_run_on_ml_node: false       -> our 3-node cluster has no dedicated ML
#                                         node, so allow the model to load on data nodes
#   * model_access_control_enabled     -> keep model-group access simple for the lab
#   * native_memory_threshold: 99      -> don't refuse a small model on a trial cluster
client.cluster.put_settings(
    body={
        "persistent": {
            "plugins.ml_commons.allow_registering_model_via_url": True,
            "plugins.ml_commons.only_run_on_ml_node": False,
            "plugins.ml_commons.model_access_control_enabled": False,
            "plugins.ml_commons.native_memory_threshold": 99,
        }
    }
)
print("Cluster settings updated for ML Commons model registration/deployment")

# Create a model group to organize registered models. ML Commons attaches an
# access policy at the group level, so you typically have one group per use case.
# The response includes ``model_group_id`` — pass it to 02-register-model.py.
response = client.transport.perform_request(
    "POST",
    "/_plugins/_ml/model_groups/_register",
    body={
        "name": "huggingface-models",
        "description": "A group for Hugging Face transformer models",
    },
)
print("Model group registration response:", response)
