"""Register a Hugging Face sentence-transformer model with ML Commons and wait for it.

Pipeline this lesson follows:
    001-setup.py             -> enable URL registration, create model group
    002-register-model.py    -> register the model (downloads weights, returns model_id)  <- you are here
    003-deploy-model.py      -> deploy the model so it's runnable
    004-generate-embeddings.py -> call the deployed model

Why poll?
    Model registration kicks off an async **task** that downloads the model
    artifacts and verifies them on the cluster. The HTTP call returns
    ``task_id`` right away — we then ask the cluster "is it done yet?" every
    couple of seconds until it reports COMPLETED or FAILED.
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

# Take ``model_group_id`` from the command line so the script is reusable.
# You got this value from running ``001-setup.py``.
if len(sys.argv) < 2:
    # Exiting with non-zero status signals failure to shells / CI runners.
    print("Usage: python 002-register-model.py <model_group_id>", file=sys.stderr)
    sys.exit(1)

model_group_id = sys.argv[1]

# Register the Hugging Face model with ML Commons. The ``name`` follows the
# convention "huggingface/<org>/<model>"; ``version`` and ``model_format``
# must match what ML Commons published for this model.
# ``TORCH_SCRIPT`` = a TorchScript serialization of the PyTorch model. The
# other option is ``ONNX``. The cluster picks the right inference engine based
# on this value.
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

# The response shape varies between cluster versions. Sometimes registration is
# synchronous and we get the ``model_id`` directly; usually we get a ``task_id``
# and have to poll. Defensive ``.get`` + ``isinstance`` handles both shapes.
task_id = response.get("task_id") if isinstance(response, dict) else None
if task_id:
    print(f"Polling task {task_id} until complete...")
    # ``poll_ml_task`` lives in ``utils/opensearch_ml.py`` — sleeps and checks
    # ``GET /_plugins/_ml/tasks/{id}`` until terminal state or timeout.
    final = poll_ml_task(client, task_id)
    print("Task result:", json.dumps(final, indent=2, default=str))
    state = final.get("state") if isinstance(final, dict) else None
    # Exit non-zero on failure so a CI run / lab harness can tell that ingestion
    # of the model didn't actually work. Look in ``final["model_id"]`` for the
    # value the deploy script needs.
    if state == "FAILED":
        print("Model registration task failed.", file=sys.stderr)
        sys.exit(1)
    if state == "TIMEOUT":
        print("Timed out waiting for model registration task.", file=sys.stderr)
        sys.exit(1)
else:
    print("No task_id in response; cluster may have applied registration synchronously.")
