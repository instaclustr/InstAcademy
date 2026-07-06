"""Lesson 2-2 Step 13: hybrid (neural + keyword) search on vector-search-index.

What this teaches:
    * The ``neural`` query — feeds query text through the same model used at index
      time, then does ANN search on the resulting vector.
    * The classic ``match`` (BM25) query — lexical, full-text.
    * Combining the two inside ``bool.should`` with ``script_score`` weights: a
      hand-rolled hybrid baseline. (Chapter 3 introduces the dedicated ``hybrid``
      query + normalization pipelines for cleaner score combination.)
"""

import os
import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from dotenv import load_dotenv

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"
load_dotenv(_ENV_FILE)

client = open_search_client_from_env_file(_ENV_FILE)
print_opensearch_connection_test(client, raise_on_error=True)

index_name = "vector-search-index"
# Reuse the index-time model so query and stored vectors live in the same space.
model_id = os.getenv("ML_MODEL_ID")
query_text = "historical fiction with an underdog story"

response = client.search(
    index=index_name,
    body={
        "_source": {"excludes": ["passage_embedding"]},
        "query": {
            "bool": {
                # Toy filter so the lesson shows filtering + scoring together.
                "filter": {"wildcard": {"id": "*1"}},
                "should": [
                    {
                        "script_score": {
                            "query": {
                                "neural": {
                                    "passage_embedding": {
                                        "query_text": query_text,
                                        "model_id": model_id,
                                        # Nearest neighbors per shard before merge.
                                        "k": 100,
                                    }
                                }
                            },
                            "script": {"source": "_score * 1.5"},
                        }
                    },
                    {
                        "script_score": {
                            "query": {"match": {"passage_text": query_text}},
                            "script": {"source": "_score * 1.7"},
                        }
                    },
                ],
            }
        },
    },
)

hits = response.get("hits", {})
total = hits.get("total", {})
if isinstance(total, dict):
    total = total.get("value", 0)
print(f"Total hits: {total}")
print("\nTop results:")
for hit in hits.get("hits", [])[:10]:
    src = hit.get("_source", {})
    print(f"  id={src.get('id')} score={hit.get('_score')} title={src.get('title', '')[:50]}...")
