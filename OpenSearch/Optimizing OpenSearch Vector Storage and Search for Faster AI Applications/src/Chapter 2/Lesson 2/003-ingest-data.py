"""Load sample-data.json and bulk-ingest each book into vector-search-index.

What this script teaches:
    * Reading the dataset produced by Chapter 1's ``data-loader.py``.
    * Bulk indexing dozens of documents with the OpenSearch bulk API.
    * How the ingest pipeline (set as ``default_pipeline`` in 002) transparently
      generates embeddings for ``passage_text`` — we never compute vectors here.

Because the index has ``default_pipeline: vector-search-embeddings-pipeline``,
each indexed doc gets a ``passage_embedding`` filled in server-side.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

import json


# Configure your OpenSearch connection.
client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# Load sample-data.json from ``src/sample-data.json`` (written by
# Chapter 1's data-loader). Keeping the file at the ``src/`` root means every
# lesson can locate it with the same ``parents[2]`` walk.
script_dir = Path(__file__).resolve().parents[2]
sample_data_path = script_dir / "sample-data.json"
with open(sample_data_path, encoding="utf-8") as f:
    data = json.load(f)

books = data.get("results", [])
index_name = "vector-search-index"

# Build bulk actions: for each book, index into vector-search-index with the required fields.
def doc_for_book(book):
    """Reshape a Gutendex book record into our index's mapping.

    Gutendex returns rich nested data; we only keep what's useful for search.
    ``passage_text`` is what the ingest pipeline embeds — we pull the first
    summary if present, falling back to an empty string for books with none.
    """
    summaries = book.get("summaries") or []
    passage_text = summaries[0] if summaries else ""
    return {
        # ``id`` here is a *field* in the doc (used as a wildcard target in
        # search), separate from the ``_id`` on the action line below.
        "id": str(book.get("id", "")),
        "title": book.get("title", ""),
        "authors": book.get("authors", []),
        "subjects": book.get("subjects", []),
        "passage_text": passage_text,
        "bookshelves": book.get("bookshelves", []),
    }

# Bulk format: alternating action header + document. Using the book's id as
# ``_id`` makes re-runs idempotent (no duplicate documents).
actions = []
for book in books:
    doc = doc_for_book(book)
    actions.append({"index": {"_index": index_name, "_id": doc["id"]}})
    actions.append(doc)

# ``request_timeout=60`` — bulk requests through an ingest pipeline that runs
# a model can be slow on cold clusters, so we give the server a generous
# window before the client gives up.
response = client.bulk(body=actions, request_timeout=60)
# Bulk responses are per-item; ``error`` only appears for failures. Counting
# them tells us if any docs were silently rejected (commonly: dimension mismatch).
failed = [
    item
    for item in response.get("items", [])
    if "error" in item.get("index", item.get("index", {}))
]
num_failed = len(failed)
num_ok = len(books) - num_failed
if num_failed:
    print(f"Bulk ingest: {num_ok} succeeded, {num_failed} failed")
    # Print only the first 5 errors so the output stays readable even when
    # something is broadly broken.
    for item in failed[:5]:
        print("  ", item.get("index", item))
    if num_failed > 5:
        print(f"  ... and {num_failed - 5} more")
else:
    print(f"Ingested {len(books)} books into {index_name}")
