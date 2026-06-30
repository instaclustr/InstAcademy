"""Create ``book-embeddings-v2`` — first iteration of a versioned embedding index.

What's the point of "v2"?
    Embedding models change. When you upgrade to a new model, you cannot just
    re-embed into the same index (different vector dims, different similarity
    properties). Instead you:
        * Create ``book-embeddings-v2`` with the new dim / parameters.
        * Backfill it from your source data.
        * Atomically switch a search alias from v1 -> v2.

Versioning the index name lets you keep the old version online during the
backfill, then cut over in one alias swap (see Lesson 2's shrink script for
the alias-swap pattern).
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, src_env_file

import json



def main() -> None:
    client = open_search_client_from_env_file(src_env_file(__file__))
    index_name = "book-embeddings-v2"
    # Recreate so the demo is reproducible. Production cutovers do NOT
    # delete the previous version until the alias swap is complete.
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)

    response = client.indices.create(
        index=index_name,
        body={
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 1,
                # k-NN plugin enabled — required for knn_vector queries.
                "index.knn": True,
            },
            "mappings": {
                "properties": {
                    "book_id": {"type": "keyword"},
                    "title": {"type": "text"},
                    "embedding": {
                        "type": "knn_vector",
                        # 768-dim — typical for sentence-transformer family models.
                        "dimension": 768,
                        "method": {
                            "name": "hnsw",
                            "space_type": "l2",
                            # ``faiss`` engine — better for large datasets,
                            # supports quantization variants.
                            "engine": "faiss",
                            # ef_construction=128 / m=16: balanced HNSW build settings.
                            "parameters": {"ef_construction": 128, "m": 16},
                        },
                    },
                    # Store the model identity inside each document. When you
                    # need to investigate "why is recall down?" you can verify
                    # every doc was embedded with the right model version.
                    "model_version": {"type": "keyword"},
                    # ``date`` type accepts ISO8601 strings or epoch millis.
                    "created_at": {"type": "date"},
                }
            },
        },
    )
    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    main()
