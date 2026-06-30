"""Use OpenSearch's ``_rank_eval`` API to score how good a search is on labeled data.

How rank-eval works:
    * You provide one or more "requests" — each is a real query plus a set of
      **ratings** (doc_id -> relevance score, integer >= 0).
    * OpenSearch runs the query, looks at the top-k results, and compares them
      to your ratings using the metric you pick (MRR, NDCG, precision, etc.).
    * You get back a single ``metric_score`` and per-request details.

That metric score is what you optimize when tuning hybrid weights, k values,
chunk size, etc. — without it, "improving search" is just vibes.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, src_env_file

import json


def load_query_vector() -> list[float]:
    """Reuse the stored 768-dim query vector (see Lesson 1)."""
    vector_path = Path(__file__).resolve().parent / "001-bookstore-rag-query-vector.json"
    with open(vector_path, encoding="utf-8") as f:
        return json.load(f)

def main() -> None:
    client = open_search_client_from_env_file(src_env_file(__file__))
    index_name = "bookstore-rag"
    query_text = "whale"
    query_vector = load_query_vector()

    # The body of a rank_eval request:
    #   "requests": one entry per labeled query.
    #     "id":      arbitrary name for this query (appears in details output).
    #     "request": a normal search body, but only the ``query`` clause matters.
    #     "ratings": ground truth: rating 0 = irrelevant, higher = more relevant.
    #   "metric": which scoring formula to apply (here MRR @ k=10).
    rank_eval_body = {
        "requests": [
            {
                "id": "mystery_query",
                "request": {
                    "query": {
                        "hybrid": {
                            "queries": [
                                {"match": {"content": {"query": query_text}}},
                                {"knn": {"content_embedding": {"vector": query_vector, "k": 10}}},
                            ]
                        }
                    }
                },
                "ratings": [
                    # Doc 2701 (Moby-Dick) is rated 0 (irrelevant) — clearly
                    # wrong for a query "whale", but kept in the lesson to
                    # demonstrate how rating choices shape the metric score.
                    # Try changing this to ``"rating": 4`` and re-running.
                    {"_index": index_name, "_id": "2701", "rating": 0},
                ],
            }
        ],
        "metric": {
            # Mean Reciprocal Rank: 1 / (rank of first relevant hit).
            # Great when "is there at least one relevant result near the top?"
            # is what matters. NDCG is better when you care about full ordering.
            "mean_reciprocal_rank": {
                "k": 10,
                # A doc is "relevant" if its rating >= this threshold.
                "relevant_rating_threshold": 1,
            }
        },
    }

    # ``_rank_eval`` is exposed as a regular search API endpoint on the index.
    # The python client doesn't have a typed wrapper, so we drop to transport.
    response = client.transport.perform_request(
        "GET",
        f"/{index_name}/_rank_eval",
        body=rank_eval_body,
        timeout=60,
    )

    # ``metric_score`` averages across all requests (here we only have one).
    metric_score = response.get("metric_score")
    print(f"metric_score: {metric_score}")
    print("details:")
    print(json.dumps(response.get("details", {}), indent=2))


if __name__ == "__main__":
    main()
