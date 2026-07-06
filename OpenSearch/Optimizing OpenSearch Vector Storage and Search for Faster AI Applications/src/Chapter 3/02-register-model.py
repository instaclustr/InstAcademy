"""Register the neural sparse encoding model with ML Commons; poll until complete.

Neural sparse vs dense (Chapter 2):
    * **Dense** embeddings are fixed-size vectors (e.g. 768 floats). Every
      dimension has a value. Great recall, but every dim costs memory.
    * **Neural sparse** embeddings are a *map* from token strings to weights,
      mostly zero (only non-zero entries are stored). More interpretable
      ("which words triggered this hit?"), often cheaper at scale, and
      indexable with the ``rank_features`` type.

This registers the **bi-encoder** ``opensearch-neural-sparse-encoding-v1``,
which runs the model at both index and query time (so queries pass a
``model_id``). Doc-only variants such as ``opensearch-neural-sparse-encoding-doc-v3-distill``
run the model only at index time; swap the name/version below to use one.

Usage: python 02-register-model.py <model_group_id>
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
    print("Usage: python 02-register-model.py <model_group_id>", file=sys.stderr)
    sys.exit(1)

model_group_id = sys.argv[1]

response = client.transport.perform_request(
    "POST",
    "/_plugins/_ml/models/_register",
    body={
        "name": "amazon/neural-sparse/opensearch-neural-sparse-encoding-v1",
        "version": "1.0.1",
        "model_group_id": model_group_id,
        "model_format": "TORCH_SCRIPT",
    },
)
print("Model registration response:", response)

# Async pattern: task_id returned, poll until COMPLETED.
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
    if isinstance(final, dict) and final.get("model_id"):
        print(f"\nSparse model_id: {final['model_id']}")
        print("Deploy it next: python 03-deploy-model.py", final["model_id"])
else:
    print("No task_id in response; cluster may have applied registration synchronously.")
