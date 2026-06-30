"""Deploy a registered ML model (POST /_plugins/_ml/models/{model_id}/_deploy).

Pass the model_id from registration (task result). Usage::

    python 003-deploy-model.py <model_id>

Or set ``ML_MODEL_ID`` if you prefer env over argv.

Polls the ML deploy task when the cluster returns ``task_id``.
"""

import json
import os
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file
from utils.opensearch_ml import poll_ml_task

client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# CLI arg > env var, mirroring 002-register-model.py.
if len(sys.argv) >= 2:
    model_id = sys.argv[1]
else:
    model_id = os.getenv("ML_MODEL_ID")

if not model_id:
    print("Usage: python 003-deploy-model.py <model_id>", file=sys.stderr)
    sys.exit(1)

# Loads model weights into JVM memory so the cluster can serve predictions.
response = client.transport.perform_request(
    "POST",
    f"/_plugins/_ml/models/{model_id}/_deploy",
)
print(json.dumps(response, indent=2, default=str))

# Async task pattern (see utils/opensearch_ml.py).
task_id = response.get("task_id") if isinstance(response, dict) else None
if task_id:
    print(f"Polling deploy task {task_id} until complete...")
    final = poll_ml_task(client, task_id)
    print("Task result:", json.dumps(final, indent=2, default=str))
    state = final.get("state") if isinstance(final, dict) else None
    if state == "FAILED":
        print("Model deploy task failed.", file=sys.stderr)
        sys.exit(1)
    if state == "TIMEOUT":
        print("Timed out waiting for model deploy task.", file=sys.stderr)
        sys.exit(1)
else:
    print("No task_id in response; deploy may have completed synchronously.")
