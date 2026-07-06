"""Hybrid search on my-sparse-neural-index using the normalization pipeline.

Teaches:
    * The dedicated ``hybrid`` query — clean replacement for a hand-rolled
      bool/should hybrid. Supports up to 5 sub-queries.
    * ``neural_sparse`` — runs the sparse model on the query text and matches
      against the doc's ``rank_features`` field.
    * The ``nested`` wrapper with ``score_mode: max`` — each doc has many
      per-chunk encodings; we score it by its best chunk.

``search_pipeline=nlp-search-normalization-pipeline`` (from
``08-normalization-pipeline.py``) rescales the keyword and sparse scores to a
comparable range before combining them.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"
load_dotenv(_ENV_FILE)

client = open_search_client_from_env_file(_ENV_FILE)
print_opensearch_connection_test(client, raise_on_error=True)

INDEX = "my-sparse-neural-index"
SEARCH_PIPELINE = "nlp-search-normalization-pipeline"
QUERY_TEXT = "a hero on a dangerous sea voyage"
model_id = (os.environ.get("ML_MODEL_ID") or "").strip()
if not model_id:
    print("Set ML_MODEL_ID in src/.env (deployed sparse encoding model).", file=sys.stderr)
    sys.exit(1)

response = client.search(
    index=INDEX,
    body={
        "_source": {"excludes": ["passage_embedding", "passage_chunk"]},
        "size": 5,
        "query": {
            "hybrid": {
                # Sub-query order must match the pipeline ``weights`` order:
                # index 0 -> match (0.3), index 1 -> neural_sparse (0.7).
                "queries": [
                    {"match": {"passage_text": {"query": QUERY_TEXT}}},
                    {
                        "nested": {
                            "path": "passage_embedding",
                            "score_mode": "max",
                            "query": {
                                "neural_sparse": {
                                    "passage_embedding.sparse_encoding": {
                                        "query_text": QUERY_TEXT,
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
    params={"search_pipeline": SEARCH_PIPELINE},
)

print("=== Hybrid (normalized) ranking ===")
for i, hit in enumerate(response.get("hits", {}).get("hits", [])[:5], start=1):
    src = hit.get("_source", {})
    print(f"  {i}. score={hit.get('_score'):.4f} id={src.get('id')} title={src.get('title', '')[:60]}")
print("\nCompare with the lexical/sparse lists from 07-compare-single-methods.py.")
