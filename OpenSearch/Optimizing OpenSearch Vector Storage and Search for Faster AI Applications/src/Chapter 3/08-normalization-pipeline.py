"""Create a search pipeline for hybrid search (score normalization + combination).

Ingest pipeline vs search pipeline:
    * Ingest pipeline runs on every incoming **document** before it's stored.
    * Search pipeline runs on every **search request/response**.

This pipeline does **score normalization**, which fixes a core hybrid-search
problem: BM25 (keyword) scores and sparse scores live on different scales, so
adding them directly biases toward whichever produces bigger numbers.
Normalization rescales each branch to a common range before combining.

Queries run with ``?search_pipeline=nlp-search-normalization-pipeline`` apply
this automatically (see ``09-hybrid-search.py``).
"""

import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"

client = open_search_client_from_env_file(_ENV_FILE)
print_opensearch_connection_test(client, raise_on_error=True)

pipeline_id = "nlp-search-normalization-pipeline"
response = client.transport.perform_request(
    "PUT",
    f"/_search/pipeline/{pipeline_id}",
    body={
        "description": "Post processor for hybrid search",
        # ``phase_results_processors`` run after each sub-query gathers its hits
        # but before OpenSearch merges them — the right moment to rescale scores.
        "phase_results_processors": [
            {
                "normalization-processor": {
                    # ``min_max``: rescale each sub-query's scores to [0, 1].
                    # Other options: ``l2``, ``z_score``.
                    "normalization": {"technique": "min_max"},
                    "combination": {
                        # ``arithmetic_mean``: weighted average of the branches.
                        # ``weights`` has one entry per sub-query and sums to 1.0.
                        # Here we trust sparse (0.7) more than keyword (0.3).
                        "technique": "arithmetic_mean",
                        "parameters": {"weights": [0.3, 0.7]},
                    },
                }
            }
        ],
    },
)
print(f"Created search pipeline: {pipeline_id}")
print("Response:", response)
