"""Register all-mpnet-base-v2 with ML Commons (POST /_plugins/_ml/models/_register).

Matches the Dev Tools body: name, version, model_format. Many clusters also require
``model_group_id`` — pass it as ``argv[1]`` or set ``ML_MODEL_GROUP_ID``. Polls the
ML task when the cluster returns ``task_id``.

About this model:
    ``sentence-transformers/all-mpnet-base-v2`` produces 768-dim sentence
    embeddings and is one of the strongest general-purpose dense encoders.
    Slower than distilbert but consistently higher recall.
"""

import json
import os
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file
from utils.opensearch_ml import poll_ml_task

client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# Two ways to supply the model group id: CLI arg wins over env var. This is
# a friendlier UX than Chapter 2's pure-positional version — you can either
# pass it inline or set it once and forget it.
_model_group_id = os.environ.get("ML_MODEL_GROUP_ID")
if len(sys.argv) >= 2:
    _model_group_id = sys.argv[1]

body: dict[str, str] = {
    "name": "huggingface/sentence-transformers/all-mpnet-base-v2",
    "version": "1.0.1",
    # ``TORCH_SCRIPT`` = TorchScript model artifacts (PyTorch). Other valid
    # value is ``ONNX``.
    "model_format": "TORCH_SCRIPT",
}
if _model_group_id:
    body["model_group_id"] = _model_group_id

# Generous timeout — registering a model triggers a download of weights
# (hundreds of MB) on the cluster side.
response = client.transport.perform_request(
    "POST",
    "/_plugins/_ml/models/_register",
    body=body,
    timeout=60,
)
print(json.dumps(response, indent=2, default=str))

# Same task-polling pattern used everywhere model registration appears.
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
else:
    print("No task_id in response; cluster may have applied registration synchronously.")
