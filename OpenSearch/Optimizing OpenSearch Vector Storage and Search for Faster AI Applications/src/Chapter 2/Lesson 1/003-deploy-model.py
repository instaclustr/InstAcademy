"""Deploy a registered ML model; poll deploy task until complete when task_id is returned.

In ML Commons there are two distinct steps for getting a model usable:
    1. **Register** (script 002) — uploads/downloads the model weights and
       metadata into the cluster. The model now exists, but no node has it
       loaded into memory.
    2. **Deploy** (this script) — pins the model into memory on one or more
       nodes so that ``_predict`` calls can run inference against it.

Undeploying frees node memory; re-deploying is fast because the artifacts are
already on disk.
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

# ``model_id`` is the value the registration task printed (look for the
# ``model_id`` field in script 002's output).
if len(sys.argv) < 2:
    print("Usage: python 003-deploy-model.py <model_id>", file=sys.stderr)
    sys.exit(1)

model_id = sys.argv[1]

# POST /_plugins/_ml/models/{model_id}/_deploy
# Deploy = load the model into JVM memory on cluster nodes. Like registration,
# this is async on bigger models, so we get back a ``task_id`` to poll.
response = client.transport.perform_request(
    "POST",
    f"/_plugins/_ml/models/{model_id}/_deploy",
)
print("Model deployment response:", response)

task_id = response.get("task_id") if isinstance(response, dict) else None
if task_id:
    print(f"Polling deploy task {task_id} until complete...")
    # Same polling helper as registration — both produce ML Commons tasks.
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
