"""Create ``book-embeddings-v3`` — bigger dimensions, higher-quality HNSW graph.

Diff vs ``book-embeddings-v2``:
    * ``dimension``: 768 -> 1024 (switched to a larger model).
    * ``ef_construction``: 128 -> 256 (more thorough graph build, slower index,
      higher recall).
    * ``m``: 16 -> 32 (more neighbor links per node — denser graph, larger
      memory footprint, better recall).
    * Added ``model_name`` for explicit per-doc tracking of which model
      produced each embedding.

This is exactly the kind of "v3" change you'd make when an evaluation
(``Chapter 4 Lesson 3 / 02-rank-eval.py``) showed v2 wasn't recalling enough.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, src_env_file

import json



def main() -> None:
    client = open_search_client_from_env_file(src_env_file(__file__))
    index_name = "book-embeddings-v3"
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)

    response = client.indices.create(
        index=index_name,
        body={
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 1,
                "index.knn": True,
            },
            "mappings": {
                "properties": {
                    "book_id": {"type": "keyword"},
                    "title": {"type": "text"},
                    "embedding": {
                        "type": "knn_vector",
                        # 1024-dim — must match whatever the new embedding
                        # model outputs (e.g. some BGE / e5-large variants).
                        "dimension": 1024,
                        "method": {
                            "name": "hnsw",
                            "space_type": "l2",
                            "engine": "faiss",
                            # Beefier HNSW parameters:
                            #   ef_construction=256: graph build searches twice
                            #     as many candidates per insertion - slower
                            #     ingest, higher graph quality.
                            #   m=32: twice as many connections per node -
                            #     bigger graph, more memory, better recall.
                            "parameters": {"ef_construction": 256, "m": 32},
                        },
                    },
                    # Two-field model identity: version + name. Lets you
                    # distinguish "same model, new fine-tune" from
                    # "completely different model".
                    "model_version": {"type": "keyword"},
                    "model_name": {"type": "keyword"},
                    "created_at": {"type": "date"},
                }
            },
        },
    )
    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    main()
