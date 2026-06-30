"""Deploy the neural sparse model so it can serve predictions.

Same two-step pattern as Chapter 2:
    register (writes weights/metadata into the cluster)
        -> deploy (loads the model into node memory so it can run)

After this completes you should put the deployed model's id into
``ML_MODEL_ID`` in ``src/.env`` — the next scripts use it from there.
"""

import json
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file
from utils.opensearch_ml import poll_ml_task

client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client)

if len(sys.argv) < 2:
    print("Usage: python 001b-deploy-model.py <model_id>", file=sys.stderr)
    sys.exit(1)

model_id = sys.argv[1]

# POST /_plugins/_ml/models/{model_id}/_deploy
# Loads model weights into JVM memory on the assigned data nodes.
response = client.transport.perform_request(
    "POST",
    f"/_plugins/_ml/models/{model_id}/_deploy",
)
print("Model deployment response:", response)

# Deploy can also return ``task_id`` — same polling pattern as registration.
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
