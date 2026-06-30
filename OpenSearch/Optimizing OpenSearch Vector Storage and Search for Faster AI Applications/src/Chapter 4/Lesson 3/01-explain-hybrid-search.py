"""Run a hybrid search with ``explain=true`` to see how each score was produced.

What this script teaches:
    * The ``explain`` parameter — OpenSearch returns a tree of
      sub-scorers and weights describing exactly how each hit's score was
      computed. Indispensable when relevance feels wrong and you need to know why.
    * Reading those explanations: each branch has a description, value, and
      list of contributing details (BM25 terms, vector similarity, etc.).
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
    """Read the pre-baked 768-dim query vector from disk.

    Same trick as Chapter 4 Lesson 1 — checking the vector in means you can
    run hybrid searches without first deploying a model.
    """
    vector_path = Path(__file__).resolve().parent / "001-bookstore-rag-query-vector.json"
    with open(vector_path, encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    client = open_search_client_from_env_file(src_env_file(__file__))
    index_name = "bookstore-rag"
    query_text = "whale"
    query_vector = load_query_vector()

    response = client.search(
        index=index_name,
        params={
            # Apply the hybrid pipeline created in Lesson 1 — score normalization.
            "search_pipeline": "bookstore-hybrid-pipeline",
            # The star of this script: include per-hit "_explanation" detailing
            # how the score breaks down across BM25 + k-NN branches.
            "explain": "true",
        },
        body={
            "query": {
                "hybrid": {
                    "queries": [
                        # BM25 lexical match on the full ``content`` field.
                        {"match": {"content": {"query": query_text}}},
                        # Vector k-NN — using a stored vector rather than ``neural``
                        # because this lab doesn't depend on a deployed model.
                        {"knn": {"content_embedding": {"vector": query_vector, "k": 10}}},
                    ]
                }
            },
        },
    )

    print("Top hits:")
    for hit in response.get("hits", {}).get("hits", []):
        source = hit.get("_source", {})
        print(f"- id={hit.get('_id')} score={hit.get('_score')} title={source.get('title')}")
        # ``_explanation`` is a recursive tree: description (English label),
        # value (this subscore), details (children that contributed).
        # Pretty-print it so you can pick apart how each clause weighed in.
        print(f"  explanation: {json.dumps(hit.get('_explanation'), indent=2)}")

if __name__ == "__main__":
    main()
