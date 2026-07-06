"""Lesson 2-1 Step 4: register msmarco-distilbert-base-tas-b and poll the task.

Pipeline this chapter follows:
    01-setup.py              -> enable settings, create model group
    02-register-model.py     -> register the model (downloads weights, returns model_id)  <- here
    03-deploy-model.py       -> deploy the model so it's runnable
    04-generate-embeddings.py -> call the deployed model

Why poll?
    Registration kicks off an async **task** that downloads and verifies the
    model artifact. The HTTP call returns ``task_id`` right away; we then ask the
    cluster "is it done yet?" every couple of seconds until COMPLETED or FAILED.
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

# ``model_group_id`` comes from running 01-setup.py.
if len(sys.argv) < 2:
    print("Usage: python 02-register-model.py <model_group_id>", file=sys.stderr)
    sys.exit(1)

model_group_id = sys.argv[1]

# Register the pretrained model. ``version`` and ``model_format`` must match what
# the OpenSearch pretrained-model repository publishes (1.0.3 / TORCH_SCRIPT ->
# 768-dim vectors). ``TORCH_SCRIPT`` is a TorchScript serialization; ``ONNX`` is
# the alternative — the cluster picks the inference engine from this value.
response = client.transport.perform_request(
    "POST",
    "/_plugins/_ml/models/_register",
    body={
        "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
        "version": "1.0.3",
        "model_group_id": model_group_id,
        "model_format": "TORCH_SCRIPT",
    },
)
print("Model registration response:", response)

# Response shape varies: usually a ``task_id`` to poll, sometimes a synchronous
# ``model_id``. Defensive ``.get`` handles both.
task_id = response.get("task_id") if isinstance(response, dict) else None
if task_id:
    print(f"Polling task {task_id} until complete...")
    final = poll_ml_task(client, task_id)
    print("Task result:", json.dumps(final, indent=2, default=str))
    state = final.get("state") if isinstance(final, dict) else None
    if state == "FAILED":
        print("Model registration task failed.", file=sys.stderr)
        sys.exit(1)
    if state == "TIMEOUT":
        print("Timed out waiting for model registration task.", file=sys.stderr)
        sys.exit(1)
    # ``final["model_id"]`` is the value the deploy script needs — save it.
    print("Save this model_id for 03-deploy-model.py and src/.env (ML_MODEL_ID).")
else:
    print("No task_id in response; cluster may have applied registration synchronously.")
