"""Dimension reduction by rebuilding into a smaller index (README Steps 26-29).

What this script teaches:
    * The ``knn_vector`` field type with HNSW on the Faiss engine (the default).
    * The ``_reindex`` API — copy/transform documents from one index to another in
      one server-side operation.
    * **Painless**, OpenSearch's scripting language, used here to truncate a
      256-dim vector to 128 dims as each document is copied.

Why truncate dimensions?
    Vector memory grows linearly with dimensions. Halving the dimensions roughly
    halves the HNSW graph memory footprint, often with only a small hit to recall.
    Rebuilding into a NEW index (rather than editing in place) is the safer,
    easy-to-roll-back approach the lesson recommends.
"""

import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file

SOURCE_INDEX = "my-vector-index"
DEST_INDEX = "my-optimized-vector-index"
SOURCE_DIM = 256
TRUNC_DIM = 128


def sample_vector(dim: int, seed: float) -> list[float]:
    """Deterministic floats in [0, 1) for a reproducible demo.

    Real applications get vectors from an embedding model (Chapter 2+). A fixed
    formula keeps the test data identical on every machine.
    """
    return [((i * 0.017 + seed) % 1.0) for i in range(dim)]


def knn_index_body(dim: int) -> dict:
    """A single-field knn_vector index using HNSW on the Faiss engine."""
    return {
        "settings": {"index": {"knn": True}},
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "my_vector": {
                    "type": "knn_vector",
                    "dimension": dim,
                    "space_type": "l2",
                    # faiss is the default engine in OpenSearch 3.x; nmslib is
                    # deprecated. lucene is the other supported option.
                    "method": {"name": "hnsw", "engine": "faiss"},
                },
            }
        },
    }


client = open_search_client_from_env_file(_SRC_ROOT / ".env")

# Clean slate. Delete dest before source so the source still exists if you decide
# to inspect it manually between deletes.
for name in (DEST_INDEX, SOURCE_INDEX):
    if client.indices.exists(index=name):
        client.indices.delete(index=name)

client.indices.create(index=SOURCE_INDEX, body=knn_index_body(SOURCE_DIM))
print(f"Created '{SOURCE_INDEX}' (knn_vector dim={SOURCE_DIM}).")

sample_docs = [
    {"_id": "1", "title": "Intro to search", "my_vector": sample_vector(SOURCE_DIM, 0.1)},
    {"_id": "2", "title": "Vectors in practice", "my_vector": sample_vector(SOURCE_DIM, 0.3)},
    {"_id": "3", "title": "Scaling retrieval", "my_vector": sample_vector(SOURCE_DIM, 0.55)},
]

# Bulk API: alternating action line (index + _id) then source document.
actions: list[dict] = []
for doc in sample_docs:
    src = {k: v for k, v in doc.items() if k != "_id"}
    actions.append({"index": {"_index": SOURCE_INDEX, "_id": doc["_id"]}})
    actions.append(src)

bulk_resp = client.bulk(body=actions)
errs = [item for item in bulk_resp.get("items", []) if "error" in item.get("index", {})]
if errs:
    raise RuntimeError(f"Bulk index failed: {errs[:3]}")
print(f"Indexed {len(sample_docs)} documents into '{SOURCE_INDEX}'.")

# Make documents visible to ``_reindex`` immediately.
client.indices.refresh(index=SOURCE_INDEX)

client.indices.create(index=DEST_INDEX, body=knn_index_body(TRUNC_DIM))
print(f"Created empty '{DEST_INDEX}' (knn_vector dim={TRUNC_DIM}).")

# ``subList(0, N)`` is Java's List API (Painless runs on the JVM): it keeps the
# first N elements, truncating each 256-dim vector to 128. The destination mapping
# must match ``TRUNC_DIM`` or indexing fails with a dimension-mismatch error.
reindex_body = {
    "source": {"index": SOURCE_INDEX},
    "dest": {"index": DEST_INDEX},
    "script": {
        "source": f"ctx._source.my_vector = ctx._source.my_vector.subList(0, {TRUNC_DIM});",
        "lang": "painless",
    },
}

response = client.reindex(body=reindex_body, wait_for_completion=True)
print("Reindex response:", response)

# ``_reindex`` does not refresh the destination index. Without this, a search
# run immediately afterward can come back empty (near-real-time visibility),
# not because the documents failed to land.
client.indices.refresh(index=DEST_INDEX)

verify = client.search(index=DEST_INDEX, body={"size": 3, "_source": ["title"]})
titles = [hit["_source"]["title"] for hit in verify["hits"]["hits"]]
print(f"Verified '{DEST_INDEX}' contains {verify['hits']['total']['value']} docs: {titles}")
