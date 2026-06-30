"""Hybrid search on my-sparse-neural-index with a search pipeline.

What this script teaches:
    * The dedicated ``hybrid`` query type — clean replacement for the
      Chapter 2 hand-rolled bool/should hybrid.
    * The ``neural_sparse`` query — runs the sparse model on your query text
      and matches against the doc's ``rank_features`` field.
    * The ``nested`` query wrapper — required because each doc has many
      per-chunk sparse encodings stored under ``passage_embedding``. We pick
      the **best** chunk per doc with ``score_mode: max``.

The ``search_pipeline`` param runs the normalization pipeline from
``002-post-processing-pipeline.py``, so the keyword and sparse scores get
rescaled to a comparable range before they're combined.
"""

import json
import os
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import (
    load_src_dotenv,
    open_search_client_from_env_file,
    print_opensearch_connection_test,
    src_env_file,
)

load_src_dotenv(__file__)

client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

index_name = "my-sparse-neural-index"
search_pipeline_id = "nlp-search-normalization-pipeline"
query_text = "a hero"
model_id = (os.environ.get("ML_MODEL_ID") or "").strip()
if not model_id:
    # Same model id used at index time has to be used at search time, otherwise
    # the query vector lives in a different feature space and recall collapses.
    print("Set ML_MODEL_ID in src/.env (deployed sparse encoding model).", file=sys.stderr)
    sys.exit(1)

response = client.search(
    index=index_name,
    body={
        # Don't return the (verbose) per-chunk sparse encodings on each hit.
        "_source": {"excludes": ["passage_embedding"]},
        "query": {
            "hybrid": {
                # ``hybrid`` runs each subquery independently and then the
                # search pipeline's normalization-processor combines scores.
                "queries": [
                    # Branch 1: BM25 keyword match against the plain text field.
                    {"match": {"passage_text": {"query": query_text}}},
                    # Branch 2: nested neural-sparse search over each chunk.
                    {
                        "nested": {
                            # Where to find the nested docs.
                            "path": "passage_embedding",
                            # Each parent doc has many chunks; ``max`` says "the
                            # parent's score is the score of its best chunk".
                            # Other options: ``avg``, ``sum``, ``none``.
                            "score_mode": "max",
                            "query": {
                                # ``neural_sparse`` encodes ``query_text`` with
                                # ``model_id`` and scores it against the
                                # ``rank_features`` field. Pure sparse retrieval,
                                # no dense vectors involved.
                                "neural_sparse": {
                                    "passage_embedding.sparse_encoding": {
                                        "query_text": query_text,
                                        "model_id": model_id,
                                    }
                                }
                            },
                        }
                    },
                ]
            }
        },
    },
    # ``search_pipeline`` activates the post-processor we created earlier.
    # Hybrid queries require a normalization pipeline — without one, scores
    # from the two branches are simply added with no rescaling.
    params={"search_pipeline": search_pipeline_id},
)

hits = response.get("hits", {})
total = hits.get("total", {})
if isinstance(total, dict):
    total = total.get("value", 0)
print(f"Total hits: {total}")
print("\nTop results:")
for hit in hits.get("hits", [])[:5]:
    src = hit.get("_source", {})
    print(f"  score={hit.get('_score')} id={src.get('id')} passage_text={str(src.get('passage_text', ''))[:80]}...")
print("\nFull response:")
print(json.dumps(response, indent=2, default=str))
