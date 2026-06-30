"""Run a hybrid (keyword + vector) search against the bookstore-rag index.

What this script teaches:
    * Using a **pre-computed** query vector from disk rather than calling the
      model at search time (handy for tutorials — the vector is checked into
      the repo so you can run this without a deployed model).
    * The ``knn`` query (raw vector input) — the bare-metal cousin of ``neural``.
    * Combining ``match`` (BM25) + ``knn`` via the ``hybrid`` query, with
      scores merged by the search pipeline created in 004.

In a real app you'd typically use ``neural`` (which embeds the query text
inside the cluster), but ``knn`` lets you bring your own vector — useful when
the client already has access to the embedding model.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

import json
import os


client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# The query vector lives next to this script — a single 768-dim list checked
# into the repo. Avoids needing a deployed model just to demo the pipeline.
_script_dir = Path(__file__).resolve().parent
_vector_path = _script_dir / "001-bookstore-rag-query-vector.json"
query_vector = json.loads(_vector_path.read_text(encoding="utf-8"))

# Environment-driven config so you can point the script at a different index /
# pipeline / query without editing code.
index_name = os.environ.get("BOOKSTORE_RAG_INDEX", "bookstore-rag-index")
search_pipeline_id = os.environ.get("BOOKSTORE_HYBRID_PIPELINE", "bookstore-hybrid-pipeline")
query_text = os.environ.get("HYBRID_MATCH_QUERY", "mystery novel under $20")

body = {
    # Don't ship the (large) embedding back with each hit.
    "_source": {"excludes": ["passage_embedding"]},
    "size": 10,
    "query": {
        "hybrid": {
            "queries": [
                # Branch 1: lexical BM25 — answers "do the same words appear?"
                {"match": {"passage_text": {"query": query_text}}},
                # Branch 2: vector k-NN — answers "is this semantically close?"
                # We pass the raw vector via ``knn`` (vs ``neural`` which would
                # call a deployed model on the cluster to embed query_text).
                {
                    "knn": {
                        "passage_embedding": {
                            "vector": query_vector,
                            # ``k`` is the per-shard candidate pool. The
                            # coordinating node sees ``k * num_shards`` candidates
                            # before final ranking.
                            "k": 10,
                        }
                    }
                },
            ]
        }
    },
}

response = client.search(
    index=index_name,
    body=body,
    # Without ``search_pipeline``, hybrid scores are added without normalization.
    params={"search_pipeline": search_pipeline_id},
)

hits = response.get("hits", {})
total = hits.get("total", {})
if isinstance(total, dict):
    total = total.get("value", 0)
print(f"Pipeline: {search_pipeline_id}  match: {query_text!r}  total hits: {total}")
print("Top results:")
for hit in hits.get("hits", []):
    src = hit.get("_source", {})
    pt = str(src.get("passage_text", ""))[:100]
    print(
        f"  score={hit.get('_score')} title={src.get('title')!r} "
        f"author={src.get('author')!r} passage_text={pt!r}..."
    )
print("\nFull response:")
print(json.dumps(response, indent=2, default=str))
