"""Chapter 4 · Step 3 — register all-mpnet-base-v2 (768-dim) and poll to COMPLETED.

Usage:
    python "src/Chapter 4/02-register-model.py" <model_group_id>
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test
from utils.opensearch_ml import poll_ml_task

if len(sys.argv) < 2:
    sys.exit('Pass the model_group_id: python "src/Chapter 4/02-register-model.py" <model_group_id>')
model_group_id = sys.argv[1]

client = open_search_client_from_env_file(_SRC / ".env")
print_opensearch_connection_test(client, raise_on_error=True)

register = client.transport.perform_request(
    "POST",
    "/_plugins/_ml/models/_register",
    body={
        "name": "huggingface/sentence-transformers/all-mpnet-base-v2",
        "version": "1.0.1",
        "model_group_id": model_group_id,
        "model_format": "TORCH_SCRIPT",
    },
)
task_id = register.get("task_id")
print("Register task:", task_id)

task = poll_ml_task(client, task_id, timeout_seconds=600)
print("Final state:", task.get("state"))
if task.get("state") == "COMPLETED":
    print("model_id:", task.get("model_id"), "— save this and set ML_MODEL_ID in src/.env after deploy.")
else:
    print("Task did not complete:", task)
