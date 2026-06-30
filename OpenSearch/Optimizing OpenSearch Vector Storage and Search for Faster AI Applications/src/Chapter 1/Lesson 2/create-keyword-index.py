"""Keyword-only bookstore demo: create a small index with text + keyword mappings and bulk sample docs.

What this script teaches:
    * The difference between ``text`` (analyzed/full-text) and ``keyword``
      (exact match, used for faceting / filtering / sorting) field types.
    * How to declare a "multi-field" so the same value can be searched both ways.
    * The shape of an OpenSearch **bulk** request body (alternating action +
      source lines, sometimes called NDJSON).
"""

import sys
from pathlib import Path

# Add ``src/`` to ``sys.path`` so shared ``utils`` imports work from Chapter 1/Lesson 2.
# Repeated in every lesson script — see ``Chapter 1/Lesson 1/opensearch-status.py``
# for a full explanation of why ``parents[2]`` resolves to ``src/``.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, src_env_file

INDEX_NAME = "keyword-index"

# Bookstore-oriented mappings: ``keyword`` types for faceting / exact match,
# ``text`` for full-text fields (analyzed, lowercased, tokenized).
# Single shard / no replica keeps the lab footprint small on a one-node cluster.
# In production you'd choose ``number_of_shards`` based on total data size and
# ``number_of_replicas >= 1`` for high availability.
INDEX_BODY = {
    "settings": {"index": {"number_of_shards": 1, "number_of_replicas": 0}},
    "mappings": {
        "properties": {
            # Multi-field: ``title`` is full-text (good for "find books about
            # mars"), while ``title.keyword`` keeps the raw value for exact
            # sorts/aggs. ``ignore_above: 256`` skips indexing oversized values
            # in the keyword sub-field so a single huge title can't blow up the
            # index.
            "title": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
            },
            # ``author`` as keyword = exact-match only. Use ``text`` instead if
            # you want "andy" to match "Andy Weir".
            "author": {"type": "keyword"},
            "isbn": {"type": "keyword"},
            "genre": {"type": "keyword"},
            "publisher": {"type": "keyword"},
            # ``description`` is free-form prose — ``text`` so the default
            # standard analyzer tokenizes it for relevance scoring.
            "description": {"type": "text"},
            "price": {"type": "float"},
            "in_stock": {"type": "boolean"},
            "published_year": {"type": "integer"},
        }
    },
}

# Hard-coded rows — no vectors; Chapter 1 Lesson 2 focuses on mappings and
# bulk indexing only. Vectors arrive in Chapter 1 Lesson 4.
SAMPLE_BOOKS = [
    {
        "isbn": "978-0143127740",
        "title": "The Martian",
        "author": "Andy Weir",
        "genre": "Science Fiction",
        "publisher": "Crown Publishing",
        "description": "An astronaut stranded on Mars fights to survive until rescue is possible.",
        "price": 16.99,
        "in_stock": True,
        "published_year": 2014,
    },
    {
        "isbn": "978-0307277677",
        "title": "The Road",
        "author": "Cormac McCarthy",
        "genre": "Fiction",
        "publisher": "Vintage",
        "description": "A father and son journey through a post-apocalyptic landscape.",
        "price": 15.95,
        "in_stock": True,
        "published_year": 2006,
    },
    {
        "isbn": "978-0061120084",
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genre": "Classic",
        "publisher": "Harper Perennial",
        "description": "A coming-of-age story set in the American South.",
        "price": 12.99,
        "in_stock": False,
        "published_year": 1960,
    },
]

# Host and credentials come from ``src/.env`` (see Chapter 1 Lesson 1).
client = open_search_client_from_env_file(
    src_env_file(__file__)
)

# Re-runs of this script must work on a clean slate. Deleting first avoids
# "mapper_parsing_exception" errors if you change ``INDEX_BODY`` between runs.
if client.indices.exists(index=INDEX_NAME):
    client.indices.delete(index=INDEX_NAME)

client.indices.create(index=INDEX_NAME, body=INDEX_BODY)
print(f"Created index '{INDEX_NAME}' with bookstore mappings.")

# OpenSearch's bulk API expects an alternating sequence:
#   line 1: action header  e.g. {"index": {"_index": "...", "_id": "..."}}
#   line 2: document source
# The python client accepts this as a flat Python list and serializes it for us.
# Using ``isbn`` as ``_id`` makes the operation idempotent — re-running won't
# create duplicate documents, it just overwrites in place.
actions: list[dict] = []
for book in SAMPLE_BOOKS:
    actions.append({"index": {"_index": INDEX_NAME, "_id": book["isbn"]}})
    actions.append(book)

bulk_response = client.bulk(body=actions)
# Bulk responses are *per-document* — the request can partially succeed.
# Always inspect ``items`` to spot mapping or version conflicts on individual docs.
failures = [item for item in bulk_response.get("items", []) if "error" in item.get("index", {})]
if failures:
    print(f"Bulk index: {len(failures)} document(s) failed")
    for item in failures[:5]:
        print(item)
else:
    print(f"Indexed {len(SAMPLE_BOOKS)} sample bookstore documents.")

# OpenSearch is "near real-time" — newly indexed docs are searchable after the
# next ``refresh`` (every 1s by default). Forcing a refresh here makes results
# visible immediately if you query right after this script runs.
client.indices.refresh(index=INDEX_NAME)
