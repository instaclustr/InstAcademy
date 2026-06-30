"""Create search pipeline ``bookstore-hybrid-pipeline`` (normalization + score combination).

Used by ``005-hybrid-search.py`` via the ``search_pipeline`` query parameter.
Mirrors::

    PUT /_search/pipeline/bookstore-hybrid-pipeline

The pipeline normalizes BM25 and k-NN scores into a comparable range, then
combines them with the weights below. Without this, a hybrid query would
just add raw scores from two very different scales — usually broken.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

import json
import os


client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# Environment override lets you swap pipelines per environment (e.g. a
# "test" pipeline with different weights) without touching the code.
pipeline_id = os.environ.get("BOOKSTORE_HYBRID_PIPELINE", "bookstore-hybrid-pipeline")

response = client.transport.perform_request(
    "PUT",
    f"/_search/pipeline/{pipeline_id}",
    body={
        "description": "Hybrid search pipeline for bookstore RAG",
        # ``phase_results_processors`` see each subquery's results before
        # they're merged — the right place to rescale scores.
        "phase_results_processors": [
            {
                "normalization-processor": {
                    "normalization": {
                        # ``min_max`` rescales each subquery's scores into [0, 1].
                        "technique": "min_max",
                    },
                    "combination": {
                        # Combined score = sum(w_i * normalized_score_i)
                        "technique": "arithmetic_mean",
                        "parameters": {
                            # First weight is for the keyword (``match``) branch,
                            # second is for the k-NN branch. Try [0.5, 0.5] or
                            # [0.7, 0.3] to see how the ranking shifts.
                            "weights": [0.3, 0.7],
                        },
                    },
                }
            }
        ],
    },
    timeout=60,
)
print(f"Put search pipeline: {pipeline_id}")
print(json.dumps(response, indent=2, default=str))
