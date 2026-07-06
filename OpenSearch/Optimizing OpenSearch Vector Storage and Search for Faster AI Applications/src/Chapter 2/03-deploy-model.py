"""Lesson 2-1 Step 5: deploy a registered model; poll the deploy task.

Two distinct steps make a model usable in ML Commons:
    1. **Register** (script 02) — downloads the weights and metadata into the
       cluster. The model exists, but no node has it loaded into memory.
    2. **Deploy** (this script) — pins the model into node memory so ``_predict``,
       ingest pipelines, and neural queries can run inference against it.

Undeploying frees node memory; re-deploying is fast because the artifacts are
already on disk.
"""

import json
import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test
from utils.opensearch_ml import poll_ml_task

_ENV_FILE = _SRC_ROOT / ".env"

client = open_search_client_from_env_file(_ENV_FILE)

print_opensearch_connection_test(client)

# ``model_id`` is the value the registration task printed.
if len(sys.argv) < 2:
    print("Usage: python 03-deploy-model.py <model_id>", file=sys.stderr)
    sys.exit(1)

model_id = sys.argv[1]

# POST /_plugins/_ml/models/{model_id}/_deploy — load into JVM/native memory on
# cluster nodes. Async on bigger models, so we get a ``task_id`` to poll.
response = client.transport.perform_request(
    "POST",
    f"/_plugins/_ml/models/{model_id}/_deploy",
)
print("Model deployment response:", response)

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
    print(f"Model {model_id} is DEPLOYED. Set ML_MODEL_ID={model_id} in src/.env")
else:
    print("No task_id in response; deploy may have completed synchronously.")
