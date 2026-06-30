"""Remove indexes and ingest pipeline created in Chapter 2 Lessons 1–2.

Why a cleanup script?
    Each chapter creates artifacts (indexes, pipelines, deployed models) that
    take up disk + memory. Running this between chapters frees those resources
    so the next chapter starts clean.

If ``ML_MODEL_ID`` is set in ``src/.env``, this also undeploys the model
(required before delete when deployed) and then deletes it from the cluster.
Order matters: indexes -> pipeline -> undeploy model -> delete model.
"""

import json
import os
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

# ``TransportError`` is the low-level HTTP/status error from opensearchpy.
# We catch it below to keep going when a resource we wanted to delete is
# already gone (404) instead of failing the entire cleanup.
from opensearchpy.exceptions import TransportError  # type: ignore[import-untyped]

from utils.opensearch_client import (
    load_src_dotenv,
    open_search_client_from_env_file,
    print_opensearch_connection_test,
    src_env_file,
)
from utils.opensearch_ml import poll_ml_task

load_src_dotenv(__file__)

# Indexes created by Chapter 2 lesson scripts (Lesson 1: none; Lesson 2: vector-search-index).
CHAPTER2_LESSON12_INDEXES = ("vector-search-index",)

# Ingest pipeline from Lesson 2 ``001-create-index-pipeline.py``.
CHAPTER2_LESSON2_PIPELINE = "vector-search-embeddings-pipeline"

client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# Delete indexes first.
# Order matters because the index has ``default_pipeline`` referencing the
# pipeline below — but deleting the pipeline while the index still references
# it is also allowed in OpenSearch, so it would technically work either way.
for index_name in CHAPTER2_LESSON12_INDEXES:
    # ``ignore_unavailable=True`` makes "index doesn't exist" a no-op instead
    # of a 404. Makes the cleanup script safe to run repeatedly.
    r = client.indices.delete(index=index_name, ignore_unavailable=True)
    if r.get("acknowledged"):
        print(f"Deleted index: {index_name}")
    else:
        print(f"Index delete response for {index_name}: {r}")

# ``ignore=[404]`` is the equivalent of ``ignore_unavailable`` for pipelines —
# don't fail if the pipeline was already missing.
r = client.ingest.delete_pipeline(id=CHAPTER2_LESSON2_PIPELINE, ignore=[404])
if r.get("acknowledged"):
    print(f"Deleted ingest pipeline: {CHAPTER2_LESSON2_PIPELINE}")
else:
    print(f"Pipeline delete response for {CHAPTER2_LESSON2_PIPELINE}: {r}")

model_id = (os.environ.get("ML_MODEL_ID") or "").strip()
if not model_id:
    # Without a model id we can't safely target the right model for deletion.
    # Skipping is better than guessing.
    print("Skipping ML model undeploy/delete: ML_MODEL_ID not set in src/.env")
else:
    # Deployed models must be undeployed before DELETE — the cluster won't let
    # you remove a model that's still loaded into node memory.
    # See: https://docs.opensearch.org/latest/ml-commons-plugin/api/model-apis/undeploy-model/
    try:
        undeploy = client.transport.perform_request(
            "POST",
            f"/_plugins/_ml/models/{model_id}/_undeploy",
        )
        print("Undeploy response:", undeploy)
        task_id = undeploy.get("task_id") if isinstance(undeploy, dict) else None
        if task_id:
            print(f"Polling undeploy task {task_id}...")
            final = poll_ml_task(client, task_id)
            print("Undeploy task result:", json.dumps(final, indent=2, default=str))
            state = final.get("state") if isinstance(final, dict) else None
            # We don't abort on undeploy failure — DELETE will surface a clear
            # error if the model is still attached, and we want to keep going.
            if state == "FAILED":
                print("Model undeploy task failed; delete may still fail.", file=sys.stderr)
            elif state == "TIMEOUT":
                print("Timed out waiting for undeploy; delete may still fail.", file=sys.stderr)
    except TransportError as exc:
        # 400 = "not deployed", 404 = "no such model". Both are fine for cleanup.
        status = getattr(exc, "status_code", None)
        if status in (400, 404):
            print(f"Undeploy not needed or skipped ({status}): {exc}")
        else:
            # Anything else (5xx, auth issues) is a real problem — re-raise.
            raise

    try:
        delete_resp = client.transport.perform_request(
            "DELETE",
            f"/_plugins/_ml/models/{model_id}",
        )
        print(f"Model deleted: {model_id}")
        print("Response:", delete_resp)
    except TransportError as exc:
        # Genuine failure — re-raise so the lab user sees the message.
        print(f"Model delete failed for {model_id}: {exc}", file=sys.stderr)
        raise
