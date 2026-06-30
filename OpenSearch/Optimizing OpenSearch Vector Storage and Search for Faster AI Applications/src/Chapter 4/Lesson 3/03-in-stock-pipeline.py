"""Create a *search* pipeline that filters results and re-scores them with a script.

Two interesting features in one pipeline:
    * ``request_processors`` run **before** the query is executed — perfect
      for injecting a filter or rewriting a query. This one wraps every search
      with a ``script_score`` so we can boost docs by a custom formula.
    * The script combines ``publish_date`` and ``ratings`` into a synthetic
      score: newer + higher-rated books float to the top.

NOTE: This is intentionally a teaching example with a couple of issues:
    1. ``"query": "in_stock: true"`` is a string, not a real filter clause —
       in production you'd write ``{"term": {"in_stock": True}}``.
    2. ``doc['publish_date'].value`` assumes ``publish_date`` is a numeric or
       date field with doc_values enabled.

The lesson's next script (``05-full-bookstore-pipeline.py``) shows a correctly-
written stock filter.
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
    pipeline_id = "bookstore-score-filter"
    # Toy query — not a real filter expression. See the file docstring.
    query_text = "in_stock: true"

    response = client.transport.perform_request(
        "PUT",
        f"/_search/pipeline/{pipeline_id}",
        body={
            "description": "Change scores on books based on ratings and publish date from search results",
            "request_processors": [
                {
                    # ``filter_query`` injects a query into the incoming request.
                    # When wrapped around ``script_score``, every match also
                    # picks up the custom score boost defined below.
                    "filter_query": {
                        "query": {
                            "script_score": {
                                "query": query_text,
                                "script": {
                                    # Painless expression — runs once per matched doc.
                                    # (publish_date - 2020) * 0.5 + ratings * 0.1
                                    # rewards both newness (years past 2020) and
                                    # rating. Tweak the weights to see how the
                                    # ranking flips.
                                    "source": "(doc['publish_date'].value - 2020)* 0.5 + doc['ratings'].value * 0.1"
                                }
                            }
                        }
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
