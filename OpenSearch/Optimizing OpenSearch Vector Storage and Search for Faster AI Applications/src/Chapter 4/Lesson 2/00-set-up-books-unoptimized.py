"""Create the ``books-unoptimized`` index — deliberately suboptimal as a starting point.

This index is the "before" picture for Chapter 4 Lesson 2's tuning exercises.
Look closely and you'll spot several issues we will fix in later scripts:

    * ``book_id``, ``isbn``, ``genre`` are mapped as ``text`` even though we
      only ever want exact matches on them. They should be ``keyword``.
    * No k-NN settings — there's no vector field at all yet.
    * No tuning of refresh interval or codec.

Later scripts in this lesson layer on chunking, vector mappings, force merge,
warmup, etc. to turn this into a production-shaped index.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

import json


client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# Basic shard / replica defaults — fine for a small lab.
_index_settings = {
    "index": {
        "number_of_shards": 2,
        "number_of_replicas": 1,
    },
}

if client.indices.exists(index="books-unoptimized"):
    # Note: this branch prints "dropping" but doesn't actually delete. The
    # condition exists so subsequent runs are no-ops on an already-created
    # index rather than throwing a "resource_already_exists_exception".
    print(f"Index books-unoptimized already exists; dropping index.")
else:
    # All fields ``text`` — looks innocent but text is analyzed (tokenized,
    # lowercased). Exact-match filters on these fields will misbehave (e.g.
    # filtering by ISBN won't work because the ISBN string gets tokenized).
    # In the next iteration we'd swap to ``keyword`` for ids and exact values.
    client.indices.create(
        index="books-unoptimized",
        body={
            "settings": _index_settings,
            "mappings": {
                "properties": {
                    "book_id": {"type": "text"},
                    "title": {"type": "text"},
                    "author": {"type": "text"},
                    "isbn": {"type": "text"},
                    "genre": {"type": "text"},
                    "published_year": {"type": "integer"},
                    "price": {"type": "float"},
                    "rating": {"type": "integer"},
                    "content": {"type": "text"},
                }
            },
        },
    )

print(f"Created index: books-unoptimized")
