"""Create the full bookstore search pipeline: request filter + result normalization.

This is the "production-ready" version that:
    1. ``request_processors``: rewrites every incoming search to require
       ``in_stock=true``. Properly written this time as a ``term`` query rather
       than the toy string from ``03-in-stock-pipeline.py``.
    2. ``phase_results_processors``: normalizes hybrid scores so keyword and
       k-NN branches end up on the same scale before being combined.

Together: customers never see out-of-stock books, AND their results are ranked
with sensibly-combined hybrid scores. Both happen automatically — the search
code calling this index doesn't have to think about either concern.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, src_env_file

import json



def main() -> None:
    client = open_search_client_from_env_file(src_env_file(__file__))
    pipeline_id = "bookstore-full-pipeline"

    response = client.transport.perform_request(
        "PUT",
        f"/_search/pipeline/{pipeline_id}",
        body={
            "description": "Full bookstore search pipeline",
            "request_processors": [
                {
                    # Inject a ``term`` filter so every query implicitly requires
                    # in_stock=true. ``tag`` is a label for this processor —
                    # surfaces in profile output for easier debugging.
                    "filter_query": {
                        "query": {
                            "term": {
                                "in_stock": True,
                            }
                        },
                        "tag": "stock_filter",
                    }
                }
            ],
            # Same normalization step we used in earlier hybrid pipelines —
            # rescale per-branch scores to [0, 1], then average with weights.
            "phase_results_processors": [
                {
                    "normalization-processor": {
                        "normalization": {
                            "technique": "min_max",
                        },
                        "combination": {
                            "technique": "arithmetic_mean",
                            "parameters": {
                                # [0.3 keyword, 0.7 vector] — same weighting
                                # as the standalone hybrid pipeline so the two
                                # pipelines stay comparable.
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


if __name__ == "__main__":
    main()
