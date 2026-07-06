"""Run the SAME hybrid query through the RRF pipeline and print the ranking.

The query body is identical to ``09-hybrid-search.py`` — only the
``search_pipeline`` differs. That's the lesson: the same two branches fused a
different way. RRF is less sensitive to outlier scores, so a doc that ranks
decently in *both* lists can overtake one that scored very high in only one.
Compare this ordering to the normalized ranking from 09.
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
SEARCH_PIPELINE = "rrf-search-pipeline"
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

print("=== Hybrid (RRF) ranking ===")
for i, hit in enumerate(response.get("hits", {}).get("hits", [])[:5], start=1):
    src = hit.get("_source", {})
    print(f"  {i}. score={hit.get('_score'):.4f} id={src.get('id')} title={src.get('title', '')[:60]}")
print("\nRRF scores are small (sums of 1/(k+rank)). Compare the ORDER to 09-hybrid-search.py.")
