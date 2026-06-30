"""Register the neural sparse encoding model with ML Commons; poll until the task completes.

Neural sparse vs dense (Chapter 2):
    * **Dense** embeddings are fixed-size vectors (e.g. 768 floats). Every
      dimension has a value. Great recall, but every dim costs memory.
    * **Neural sparse** embeddings are a *map* from token strings to weights,
      usually with mostly-zero values (so only the non-zero entries are stored).
      Better interpretability ("which words triggered this hit?"), often
      cheaper at large scale, and indexable with the ``rank_features`` type.

The model registered here turns text into sparse encodings; later scripts wire
it up to an ingest pipeline so docs get sparse vectors automatically.
"""

import json
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file
from utils.opensearch_ml import poll_ml_task

client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client)

if len(sys.argv) < 2:
    print("Usage: python 001a-register-model.py <model_group_id>", file=sys.stderr)
    sys.exit(1)

model_group_id = sys.argv[1]

# Note the different model name compared to Chapter 2: this is OpenSearch's
# own neural-sparse encoder, not a generic sentence transformer. The encoding
# format (sparse vs dense) is determined by the model architecture itself.
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

# Same async pattern as Chapter 2 — task_id returned, poll until done.
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
