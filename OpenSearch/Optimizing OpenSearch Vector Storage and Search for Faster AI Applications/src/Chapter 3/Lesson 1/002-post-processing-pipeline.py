"""Create a search pipeline for hybrid search (normalization + score combination).

What's a "search pipeline" (vs. an ingest pipeline)?
    * Ingest pipeline: runs on every incoming **document** before it's stored.
    * Search pipeline: runs on every **search request and response**.

This particular pipeline does **score normalization**, which fixes a key
problem with hybrid search: BM25 (keyword) scores and neural similarity scores
live in totally different scales (BM25 can be 0–20, neural ~0–1). Adding them
directly biases the result toward whichever query type happens to produce
bigger numbers. Normalization rescales each branch to a common range before
combining.

When the index runs queries with ``?search_pipeline=nlp-search-normalization-pipeline``,
the cluster applies this processing automatically.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file



client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# PUT /_search/pipeline/nlp-search-pipeline
pipeline_id = "nlp-search-normalization-pipeline"
response = client.transport.perform_request(
    "PUT",
    f"/_search/pipeline/{pipeline_id}",
    body={
        "description": "Post processor for hybrid search",
        # ``phase_results_processors`` run **after** each subquery has gathered
        # its own hits, but **before** OpenSearch merges them. That's exactly
        # the right moment to rescale per-query scores.
        "phase_results_processors": [
            {
                "normalization-processor": {
                    # ``min_max``: rescale each subquery's scores to [0, 1]
                    # (subtract min, divide by range). Other option is ``l2``.
                    "normalization": {"technique": "min_max"},
                    "combination": {
                        # ``arithmetic_mean``: combined = w1*s1 + w2*s2 ...
                        # ``weights`` lists must sum to 1.0 and have one entry
                        # per subquery in the hybrid query. Here we trust
                        # neural search more (0.7) than keyword (0.3).
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
