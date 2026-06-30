"""Example of reducing vector dimensions: build a small source index, then reindex with a Painless script.

What this script teaches:
    * The ``knn_vector`` field type and the HNSW algorithm OpenSearch uses for
      approximate nearest-neighbor search.
    * The ``_reindex`` API — how to copy/transform documents from one index to
      another in one server-side operation.
    * **Painless**, OpenSearch's built-in scripting language, used here to
      mutate each doc as it's copied (truncate a 256-dim vector to 128 dims).

Why bother truncating dimensions?
    Vector memory grows linearly with dimensions. Halving the dimensions also
    roughly halves the HNSW graph memory footprint, often with only a small hit
    to recall. This is the basic shape of "vector compression" experiments.
"""

import sys
from pathlib import Path

# Lesson folder is ``src/Chapter 1/1-4`` — ``parents[2]`` is the repo ``src/``
# so we can import shared ``utils``. See Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, src_env_file

# Same logical documents land in both indexes; destination stores shorter vectors
# (lower memory / slightly different ANN behavior).
SOURCE_INDEX = "my-vector-index"
DEST_INDEX = "my-optimized-vector-index"
SOURCE_DIM = 256
TRUNC_DIM = 128


def sample_vector(dim: int, seed: float) -> list[float]:
    """Deterministic floats in [0, 1) for a reproducible demo.

    Real applications get vectors from an embedding model (Chapter 2+).
    Using a deterministic formula here means the test data is identical on
    every machine, which makes the lesson easier to follow.
    """
    return [((i * 0.017 + seed) % 1.0) for i in range(dim)]


# Credentials and host come from ``src/.env`` (see Chapter 1 Lesson 1).
client = open_search_client_from_env_file(
    src_env_file(__file__)
)

# --- Source index: 256-dim knn vectors + a simple title field ---
# ``index.knn: True`` enables the k-NN plugin's special data structures on this
# index. Without it, ``knn_vector`` fields can't be queried with ``knn`` queries.
source_body = {
    "settings": {"index.knn": True},
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "my_vector": {
                "type": "knn_vector",
                "dimension": SOURCE_DIM,
                "method": {
                    # Three pluggable engines: ``lucene`` (pure Java, easiest),
                    # ``nmslib`` (legacy), ``faiss`` (richer quantization support).
                    "engine": "lucene",
                    # ``l2`` = Euclidean distance. Other options: ``cosinesimil``,
                    # ``innerproduct``. Must match how your embeddings were trained.
                    "space_type": "l2",
                    # HNSW = Hierarchical Navigable Small World — the de-facto
                    # ANN graph algorithm. Trades a tiny bit of recall for
                    # huge speedups vs. brute-force comparison.
                    "name": "hnsw",
                    "parameters": {},
                },
            },
        }
    },
}

# --- Destination index: same fields but vectors stored at 128 dims after reindex ---
dest_body = {
    "settings": {"index.knn": True},
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "my_vector": {
                "type": "knn_vector",
                "dimension": TRUNC_DIM,
                "method": {
                    "engine": "lucene",
                    "space_type": "l2",
                    "name": "hnsw",
                    "parameters": {},
                },
            },
        }
    },
}

# Clean slate so re-runs do not fail on existing mappings or document ids.
# Delete dest before source so the dest's source index still exists if you
# decide to inspect it manually between deletes.
for name in (DEST_INDEX, SOURCE_INDEX):
    if client.indices.exists(index=name):
        client.indices.delete(index=name)

client.indices.create(index=SOURCE_INDEX, body=source_body)
print(f"Created '{SOURCE_INDEX}' (knn_vector dim={SOURCE_DIM}).")

# Three made-up documents with deterministic 256-dim vectors.
sample_docs = [
    {"_id": "1", "title": "Intro to search", "my_vector": sample_vector(SOURCE_DIM, 0.1)},
    {"_id": "2", "title": "Vectors in practice", "my_vector": sample_vector(SOURCE_DIM, 0.3)},
    {"_id": "3", "title": "Scaling retrieval", "my_vector": sample_vector(SOURCE_DIM, 0.55)},
]

# Bulk API: alternating action line (index + _id) then source document.
# We strip ``_id`` from the source dict — it goes in the action line, not the body.
actions: list[dict] = []
for doc in sample_docs:
    src = {k: v for k, v in doc.items() if k != "_id"}
    actions.append({"index": {"_index": SOURCE_INDEX, "_id": doc["_id"]}})
    actions.append(src)

bulk_resp = client.bulk(body=actions)
errs = [item for item in bulk_resp.get("items", []) if "error" in item.get("index", {})]
if errs:
    # Raising here is appropriate for a lab demo — if ingest fails, the
    # subsequent ``_reindex`` step has nothing to copy.
    raise RuntimeError(f"Bulk index failed: {errs[:3]}")
print(f"Indexed {len(sample_docs)} documents into '{SOURCE_INDEX}'.")

# Make documents visible to ``_reindex`` immediately (bulk is near-real-time by default).
# Without this, ``_reindex`` could miss documents that haven't been refreshed yet.
client.indices.refresh(index=SOURCE_INDEX)

client.indices.create(index=DEST_INDEX, body=dest_body)
print(f"Created empty '{DEST_INDEX}' (knn_vector dim={TRUNC_DIM}).")

# ``_reindex`` copies each hit from ``source.index`` into ``dest.index``. The
# optional ``script`` runs server-side on each document *before* it's written
# to dest. ``ctx._source`` is the document — we mutate it in place.
#
# ``subList(0, N)`` is Java's List API (Painless runs on the JVM). It returns
# the first N elements, effectively truncating the 256-dim vector to 128.
# The destination mapping must match (``TRUNC_DIM``); otherwise indexing fails
# with a dimension-mismatch error.
reindex_body = {
    "source": {"index": SOURCE_INDEX},
    "dest": {"index": DEST_INDEX},
    "script": {
        "source": f"ctx._source.my_vector = ctx._source.my_vector.subList(0, {TRUNC_DIM});",
        "lang": "painless",
    },
}

# ``wait_for_completion=True`` makes this call block until reindex finishes.
# For large indexes you'd set ``False`` and poll the ``_tasks`` API instead.
response = client.reindex(body=reindex_body, wait_for_completion=True)
print("Reindex response:", response)
