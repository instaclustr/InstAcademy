"""Chapter 2 Cleanup (C1-C5): remove the search pipeline, index, ingest pipeline,
and optionally undeploy + delete the ML model.

Each chapter creates artifacts (search/ingest pipelines, indexes, deployed models)
that take up disk + memory. Run this between chapters to free those resources.

If ``ML_MODEL_ID`` is set in ``src/.env``, this also undeploys the model (required
before delete when deployed) and then deletes it. Order matters:
search pipeline -> index -> ingest pipeline -> undeploy model -> delete model.
"""

import json
import os
import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from dotenv import load_dotenv
from opensearchpy.exceptions import TransportError  # type: ignore[import-untyped]

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test
from utils.opensearch_ml import poll_ml_task

_ENV_FILE = _SRC_ROOT / ".env"
load_dotenv(_ENV_FILE)

SEARCH_PIPELINE = "default-model-pipeline"
INDEXES = ("vector-search-index",)
INGEST_PIPELINE = "vector-search-embeddings-pipeline"

client = open_search_client_from_env_file(_ENV_FILE)
print_opensearch_connection_test(client, raise_on_error=True)

# Delete the search pipeline (neural_query_enricher default model). ignore=[404].
try:
    client.transport.perform_request("DELETE", f"/_search/pipeline/{SEARCH_PIPELINE}")
    print(f"Deleted search pipeline: {SEARCH_PIPELINE}")
except TransportError as exc:
    if getattr(exc, "status_code", None) == 404:
        print(f"Search pipeline already gone: {SEARCH_PIPELINE}")
    else:
        raise

# Delete indexes.
for index_name in INDEXES:
    r = client.indices.delete(index=index_name, ignore_unavailable=True)
    if r.get("acknowledged"):
        print(f"Deleted index: {index_name}")
    else:
        print(f"Index delete response for {index_name}: {r}")

# Delete the ingest pipeline.
r = client.ingest.delete_pipeline(id=INGEST_PIPELINE, ignore=[404])
if r.get("acknowledged"):
    print(f"Deleted ingest pipeline: {INGEST_PIPELINE}")
else:
    print(f"Pipeline delete response for {INGEST_PIPELINE}: {r}")

model_id = (os.environ.get("ML_MODEL_ID") or "").strip()
if not model_id:
    print("Skipping ML model undeploy/delete: ML_MODEL_ID not set in src/.env")
    sys.exit(0)

# Deployed models must be undeployed before DELETE.
try:
    undeploy = client.transport.perform_request("POST", f"/_plugins/_ml/models/{model_id}/_undeploy")
    print("Undeploy response:", undeploy)
    task_id = undeploy.get("task_id") if isinstance(undeploy, dict) else None
    if task_id:
        print(f"Polling undeploy task {task_id}...")
        final = poll_ml_task(client, task_id)
        print("Undeploy task result:", json.dumps(final, indent=2, default=str))
except TransportError as exc:
    status = getattr(exc, "status_code", None)
    if status in (400, 404):
        print(f"Undeploy not needed or skipped ({status}): {exc}")
    else:
        raise

try:
    delete_resp = client.transport.perform_request("DELETE", f"/_plugins/_ml/models/{model_id}")
    print(f"Model deleted: {model_id}")
    print("Response:", delete_resp)
except TransportError as exc:
    print(f"Model delete failed for {model_id}: {exc}", file=sys.stderr)
    raise
