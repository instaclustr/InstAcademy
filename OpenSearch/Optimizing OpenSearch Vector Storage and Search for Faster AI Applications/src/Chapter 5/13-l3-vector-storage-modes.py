"""Demonstrate ``knn_vector`` storage modes: ``on_disk`` vs ``in_memory``.

Two extremes of the k-NN cost/latency trade-off:

    on_disk    — vectors live on disk; small native memory footprint.
                 Slower queries, since each vector must be read from disk
                 (page-cache permitting). Good for huge archives queried
                 rarely.

    in_memory  — vectors fully resident in native memory. Lowest latency.
                 Memory cost = num_docs * dimension * sizeof(data_type).
                 Standard production setting for hot embeddings.

You pick per index — typically:
    * Hot working set:  in_memory
    * Cold archive:     on_disk
    * Tiered cluster:   route reads to whichever copy is appropriate
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see src/Chapter 1 scripts for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file

import json



def create_or_replace_index(client: object, index_name: str, body: dict) -> dict:
    """Helper: drop the index if it exists, then create it fresh.

    Always-rebuild is the right behaviour for lab demos — but in production
    you'd never delete an index just to re-create it with different settings.
    """
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)
    return client.indices.create(index=index_name, body=body)


def main() -> None:
    client = open_search_client_from_env_file(_SRC_ROOT / ".env")

    # ``on_disk`` mode — minimal native memory use, slower queries.
    # The plugin still loads enough metadata into RAM to navigate the HNSW
    # graph, but the actual vector values are read from disk during search.
    archive_response = create_or_replace_index(
        client,
        "book-embeddings-archive",
        {
            "settings": {"index.knn": True},
            "mappings": {
                "properties": {
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": 768,
                        "mode": "on_disk",
                    }
                }
            },
        },
    )
    print("Created book-embeddings-archive:")
    print(json.dumps(archive_response, indent=2, default=str))

    # ``in_memory`` mode — vectors fully native-memory resident.
    # ``data_type: float`` is the default; alternatives like ``byte``
    # or ``binary`` trade accuracy for memory savings.
    efficient_response = create_or_replace_index(
        client,
        "book-embeddings-efficient",
        {
            "settings": {"index.knn": True},
            "mappings": {
                "properties": {
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": 768,
                        "mode": "in_memory",
                        "data_type": "float",
                    }
                }
            },
        },
    )
    print("\nCreated book-embeddings-efficient:")
    print(json.dumps(efficient_response, indent=2, default=str))

    # fp16 (SQfp16) scalar quantization — ~2x memory reduction with <1% recall
    # loss. NOTE: OpenSearch has NO ``data_type: "float16"`` (that value is
    # invalid). fp16 is configured through the Faiss ``sq`` encoder. Verified
    # live against OpenSearch 3.5: the ``sq`` encoder does NOT accept a
    # ``bits`` parameter -- ``{"name": "sq", "parameters": {"bits": 16}}``
    # fails with a mapper_parsing_exception. It only implements one
    # quantization type (fp16); its only valid sub-parameter is the optional
    # boolean ``clip``. Valid ``data_type`` values are ``float``, ``byte``,
    # ``binary``.
    fp16_response = create_or_replace_index(
        client,
        "book-embeddings-fp16",
        {
            "settings": {"index.knn": True},
            "mappings": {
                "properties": {
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": 768,
                        "space_type": "l2",
                        "method": {
                            "name": "hnsw",
                            "engine": "faiss",
                            "parameters": {
                                "encoder": {"name": "sq"},
                                "ef_construction": 128,
                                "m": 16,
                            },
                        },
                    }
                }
            },
        },
    )
    print("\nCreated book-embeddings-fp16 (Faiss SQfp16):")
    print(json.dumps(fp16_response, indent=2, default=str))


if __name__ == "__main__":
    main()
