"""Run a hybrid (neural + keyword) search on vector-search-index.

What this script teaches:
    * The ``neural`` query — feeds query text through the same model used at
      indexing time, then does a k-NN search on the resulting vector.
    * The classic ``match`` (BM25) query — lexical, full-text.
    * Combining the two inside a ``bool.should`` with ``script_score`` weights,
      a hand-rolled hybrid search. (Chapter 3+ introduces the dedicated
      ``hybrid`` query + normalization pipelines for cleaner score combination.)
"""

import os
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

import json


# Configure your OpenSearch connection.
client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# GET /vector-search-index/_search
index_name = "vector-search-index"
# Reuse the model id from ``src/.env`` so query-time and index-time embeddings
# come from the **same** model. Using two different models is the classic
# "vectors live in different spaces" bug — recall plummets.
model_id = os.getenv("ML_MODEL_ID")
query_text = "historical fiction with an underdog story"

response = client.search(
    index=index_name,
    body={
        # ``_source`` excludes the embedding so search responses stay small —
        # 768 floats per hit adds up fast.
        "_source": {"excludes": ["passage_embedding"]},
        "query": {
            # ``bool`` is the workhorse query for combining clauses:
            #   filter -> must match, doesn't affect score
            #   should -> contributes to score (any clause matching is enough)
            #   must / must_not -> match and score, or exclude
            "bool": {
                # ``wildcard`` on ``id`` is just a toy filter so the lesson can
                # show how to combine filtering with neural/keyword scoring.
                "filter": {"wildcard": {"id": "*1"}},
                "should": [
                    # Clause 1: vector search via the deployed model.
                    # ``script_score`` wraps it so we can apply a custom weight (1.5x).
                    {
                        "script_score": {
                            "query": {
                                # ``neural`` = "embed this text using model_id,
                                # then run a k-NN query against passage_embedding".
                                "neural": {
                                    "passage_embedding": {
                                        "query_text": query_text,
                                        "model_id": model_id,
                                        # ``k`` is how many nearest neighbors
                                        # the k-NN layer returns *per shard*
                                        # before the coordinating node merges
                                        # results. Higher k = better recall, more work.
                                        "k": 100,
                                    }
                                }
                            },
                            "script": {"source": "_score * 1.5"},
                        }
                    },
                    # Clause 2: lexical BM25 match on the raw text, weighted 1.7x.
                    # Boosting keyword above neural here is a deliberate
                    # demonstration — try flipping the weights to see the effect.
                    {
                        "script_score": {
                            "query": {
                                "match": {"passage_text": query_text},
                            },
                            "script": {"source": "_score * 1.7"},
                        },
                    },
                ],
            }
        },
    },
)

# OpenSearch returns hits under ``response["hits"]["hits"]`` and a total under
# ``response["hits"]["total"]`` (either an int on old versions or a dict on new ones).
hits = response.get("hits", {})
total = hits.get("total", {})
if isinstance(total, dict):
    total = total.get("value", 0)
else:
    total = total
print(f"Total hits: {total}")
print("\nTop results:")
for hit in hits.get("hits", [])[:10]:
    src = hit.get("_source", {})
    # ``_score`` is the final relevance score after the boolean combination.
    # Slicing the title keeps the console output readable.
    print(f"  id={src.get('id')} score={hit.get('_score')} title={src.get('title', '')[:50]}...")
