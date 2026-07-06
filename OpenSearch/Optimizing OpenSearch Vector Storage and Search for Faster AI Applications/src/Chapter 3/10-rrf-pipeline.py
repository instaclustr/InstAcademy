"""Create a search pipeline that fuses hybrid results with Reciprocal Rank Fusion.

Unlike the normalization pipeline (score-based), the ``score-ranker-processor``
is **rank-based**: it merges results by their rank position, not their raw
scores, using the RRF formula:

    rankScore(doc) = sum over lists j of  1 / (rank_constant + rank_j)

Because it uses ranks, RRF needs no score normalization and no labeled data to
tune weights — it "just works". ``rank_constant`` (default 60) softens the
advantage of top ranks: larger = more uniform, smaller = bigger gaps between
ranks. Weights are still optional (one per sub-query, summing to 1.0).

Run the same hybrid query through this pipeline in ``11-rrf-search.py`` and
compare the ranking to the normalized one.
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

pipeline_id = "rrf-search-pipeline"
response = client.transport.perform_request(
    "PUT",
    f"/_search/pipeline/{pipeline_id}",
    body={
        "description": "Post processor for hybrid RRF search",
        "phase_results_processors": [
            {
                "score-ranker-processor": {
                    "combination": {
                        "technique": "rrf",
                        "rank_constant": 40,
                        "parameters": {"weights": [0.7, 0.3]},
                    }
                }
            }
        ],
    },
)
print(f"Created search pipeline: {pipeline_id}")
print("Response:", response)
