"""Deploy the neural sparse model so it can serve predictions.

Two-step ML Commons pattern:
    register (writes weights/metadata into the cluster)
        -> deploy (loads the model into node memory so it can run)

After this completes, put the deployed model's id into ``ML_MODEL_ID`` in
``src/.env`` — the ingest-pipeline and search scripts read it from there.

Usage: python 03-deploy-model.py <sparse_model_id>
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

if len(sys.argv) < 2:
    print("Usage: python 03-deploy-model.py <sparse_model_id>", file=sys.stderr)
    sys.exit(1)

model_id = sys.argv[1]

# POST /_plugins/_ml/models/{model_id}/_deploy loads weights into JVM memory.
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
    print(f"\nDeployed. Add to src/.env:  ML_MODEL_ID={model_id}")
else:
    print("No task_id in response; deploy may have completed synchronously.")
    print(f"Add to src/.env:  ML_MODEL_ID={model_id}")
