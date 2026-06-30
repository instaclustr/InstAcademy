"""k-NN search on bookstore-rag-index using a stored query embedding (768-dim).

This is the simplest possible vector search:
    * No hybrid combination, no normalization pipeline.
    * Just "give me the 10 nearest neighbors of this vector".

The sample vector is in ``001-bookstore-rag-query-vector.json`` (extracted
from the original Dev Tools-style request). Override the index with
``BOOKSTORE_RAG_INDEX``.

``profile: true`` tells OpenSearch to return per-shard query timing in the
response — handy to see how much time is spent in the HNSW phase vs scoring.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

import json


client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# Pre-baked 768-dim query vector lives next to this script.
_script_dir = Path(__file__).resolve().parent
_vector_path = _script_dir / "001-bookstore-rag-query-vector.json"
query_vector = json.loads(_vector_path.read_text(encoding="utf-8"))

index_name = "bookstore-rag-index"

body = {
    "query": {
        # ``knn`` is the raw vector query: pass a vector, get nearest neighbors.
        # Contrast with ``neural``, which takes text and calls a deployed model.
        "knn": {
            "passage_embedding": {
                "vector": query_vector,
                # ``k`` per shard. With 2 shards we ask for 10 each, and the
                # coordinator merges and returns the top ``size`` (10 by default).
                "k": 10,
            }
        }
    },
    # ``profile`` adds a ``profile`` section to the response with per-shard
    # timing data — invaluable for debugging slow queries.
    "profile": "true",
    "size": 10,
    # Whitelist the small subset of fields we actually want to display.
    "_source": ["title", "author", "price", "rating", "genre"],
}

response = client.search(index=index_name, body=body, timeout=60)

hits = response.get("hits", {})
total = hits.get("total", {})
if isinstance(total, dict):
    total = total.get("value", 0)
print(f"Total hits: {total}")
print("Top results:")
for hit in hits.get("hits", []):
    src = hit.get("_source", {})
    print(
        f"  score={hit.get('_score')} title={src.get('title')!r} "
        f"author={src.get('author')!r} genre={src.get('genre')!r}"
    )
print("\nFull response:")
print(json.dumps(response, indent=2, default=str))
