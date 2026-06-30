"""Create ``my-index`` with bookstore-oriented mappings (for Lesson 2 mapping/shrink demos).

This is a tiny single-shard index used by the rest of Lesson 2 to demonstrate:
    * Reading mappings (``01-get-mapping.py``).
    * Shrinking an index (``02-shrink-index.py``).
    * Reindexing with a script transformation (``03-reindex-books.py``).

We delete and recreate so ``01-get-mapping.py`` always sees a fresh, known
mapping. Field names mirror the Chapter 1 keyword bookstore example so you
can compare them side-by-side.
"""

import json
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

INDEX_NAME = "my-index"

INDEX_BODY = {
    "settings": {
        "index": {
            # Single-shard primary, no replicas. Smallest possible index;
            # required for the shrink demo (you can only shrink to factors of
            # the current primary count, and 1 is a useful baseline).
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
    },
    "mappings": {
        "properties": {
            "book_id": {"type": "keyword"},
            "title": {
                # Multi-field: full-text + an exact-match subfield (.keyword).
                "type": "text",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
            },
            "author": {"type": "keyword"},
            "isbn": {"type": "keyword"},
            "genre": {"type": "keyword"},
            "publisher": {"type": "keyword"},
            "description": {"type": "text"},
            "price": {"type": "float"},
            "in_stock": {"type": "boolean"},
            "published_year": {"type": "integer"},
        }
    },
}


def main() -> None:
    client = open_search_client_from_env_file(src_env_file(__file__))
    print_opensearch_connection_test(client, raise_on_error=True)

    # Re-create on each run for a predictable starting state.
    if client.indices.exists(index=INDEX_NAME):
        client.indices.delete(index=INDEX_NAME)
        print(f"Deleted existing index: {INDEX_NAME}")

    response = client.indices.create(index=INDEX_NAME, body=INDEX_BODY)
    print(f"Created index: {INDEX_NAME}")
    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    main()
