"""Create the three Lesson 1-1 vector indexes: in-memory HNSW, disk-based, and memory-optimized.

What this script teaches (mirrors README Steps 2, 6, and 7):
    * A basic ``knn_vector`` field using the HNSW method on the Faiss engine
      (the default engine in OpenSearch 3.x).
    * Disk-based storage with ``mode: on_disk`` + ``compression_level`` to trade a
      little recall for large memory savings (scalar/binary quantization).
    * Memory-optimized storage with ``mode: on_disk`` + ``compression_level: 1x``
      (OpenSearch 3.1+), which memory-maps the index instead of loading it fully
      into RAM.

Engine note: ``nmslib`` is deprecated in OpenSearch 3.x — prefer ``faiss`` (used
here) or ``lucene``.
"""

import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file

DIM = 8

# Step 2: in-memory HNSW on Faiss. ``m`` and ``ef_construction`` control graph
# quality vs. build cost/memory; ``space_type`` (l2 = Euclidean) is the distance
# function and can sit at the top level of the field.
FUNDAMENTALS_INDEX = "vector-fundamentals"
FUNDAMENTALS_BODY = {
    "settings": {"index": {"knn": True, "knn.algo_param.ef_search": 100}},
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "my_vector": {
                "type": "knn_vector",
                "dimension": DIM,
                "space_type": "l2",
                "method": {
                    "name": "hnsw",
                    "engine": "faiss",
                    "parameters": {"m": 16, "ef_construction": 100},
                },
            },
        }
    },
}

# Step 6: disk-based. Setting ``mode``/``compression_level`` lets OpenSearch pick
# the engine (faiss) and a quantizing encoder; you must NOT also set method.encoder.
DISK_INDEX = "vector-disk-demo"
DISK_BODY = {
    "settings": {"index": {"knn": True}},
    "mappings": {
        "properties": {
            "my_vector": {
                "type": "knn_vector",
                "dimension": DIM,
                "space_type": "l2",
                "mode": "on_disk",
                "compression_level": "16x",
            }
        }
    },
}

# Step 7: memory-optimized = on_disk layout with no quantization (1x).
MEMOPT_INDEX = "vector-memopt-demo"
MEMOPT_BODY = {
    "settings": {"index": {"knn": True}},
    "mappings": {
        "properties": {
            "my_vector": {
                "type": "knn_vector",
                "dimension": DIM,
                "space_type": "l2",
                "mode": "on_disk",
                "compression_level": "1x",
            }
        }
    },
}

client = open_search_client_from_env_file(_SRC_ROOT / ".env")

for name, body in (
    (FUNDAMENTALS_INDEX, FUNDAMENTALS_BODY),
    (DISK_INDEX, DISK_BODY),
    (MEMOPT_INDEX, MEMOPT_BODY),
):
    # Clean slate so re-runs don't fail on existing mappings.
    if client.indices.exists(index=name):
        client.indices.delete(index=name)
    client.indices.create(index=name, body=body)
    print(f"Created '{name}'.")
