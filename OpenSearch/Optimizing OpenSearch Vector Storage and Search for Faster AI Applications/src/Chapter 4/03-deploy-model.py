"""Chapter 4 · Step 4 — deploy the registered model and poll to COMPLETED.

Usage:
    python "src/Chapter 4/03-deploy-model.py" <model_id>

After this succeeds, set ML_MODEL_ID=<model_id> in src/.env.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test
from utils.opensearch_ml import poll_ml_task

if len(sys.argv) < 2:
    sys.exit('Pass the model_id: python "src/Chapter 4/03-deploy-model.py" <model_id>')
model_id = sys.argv[1]

client = open_search_client_from_env_file(_SRC / ".env")
print_opensearch_connection_test(client, raise_on_error=True)

deploy = client.transport.perform_request("POST", f"/_plugins/_ml/models/{model_id}/_deploy")
task_id = deploy.get("task_id")
print("Deploy task:", task_id)

if task_id:
    task = poll_ml_task(client, task_id, timeout_seconds=600)
    print("Final state:", task.get("state"))
print(f"Set ML_MODEL_ID={model_id} in src/.env")
