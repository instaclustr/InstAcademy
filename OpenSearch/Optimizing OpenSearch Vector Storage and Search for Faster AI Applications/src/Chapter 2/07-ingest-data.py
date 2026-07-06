"""Lesson 2-2 Step 9: bulk-ingest books into vector-search-index.

What this teaches:
    * Reading the dataset produced by Chapter 1's ``data-loader.py``.
    * Bulk indexing dozens of documents with the OpenSearch bulk API.
    * How the ingest pipeline (set as ``default_pipeline`` in 06) transparently
      generates embeddings for ``passage_text`` — we never compute vectors here.

Because the index has ``default_pipeline: vector-search-embeddings-pipeline``,
each indexed doc gets a ``passage_embedding`` filled in server-side.
"""

import json
import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"

client = open_search_client_from_env_file(_ENV_FILE)
print_opensearch_connection_test(client, raise_on_error=True)

# ``src/sample-data.json`` lives at the src root (written by Chapter 1's loader).
sample_data_path = _SRC_ROOT / "sample-data.json"
with open(sample_data_path, encoding="utf-8") as f:
    data = json.load(f)

books = data.get("results", [])
index_name = "vector-search-index"


def doc_for_book(book):
    """Reshape a Gutendex record into the index mapping. ``passage_text`` (the
    first summary) is what the ingest pipeline embeds."""
    summaries = book.get("summaries") or []
    passage_text = summaries[0] if summaries else ""
    return {
        "id": str(book.get("id", "")),
        "title": book.get("title", ""),
        "authors": book.get("authors", []),
        "subjects": book.get("subjects", []),
        "passage_text": passage_text,
        "bookshelves": book.get("bookshelves", []),
    }


# Alternating action header + document. Using the book id as ``_id`` makes
# re-runs idempotent (no duplicate documents).
actions = []
for book in books:
    doc = doc_for_book(book)
    actions.append({"index": {"_index": index_name, "_id": doc["id"]}})
    actions.append(doc)

# Generous timeout: each doc triggers a model inference through the pipeline.
response = client.bulk(body=actions, request_timeout=60)
failed = [item for item in response.get("items", []) if "error" in item.get("index", {})]
num_failed = len(failed)
num_ok = len(books) - num_failed
if num_failed:
    print(f"Bulk ingest: {num_ok} succeeded, {num_failed} failed")
    for item in failed[:5]:
        print("  ", item.get("index", item))
    if num_failed > 5:
        print(f"  ... and {num_failed - 5} more")
else:
    print(f"Ingested {len(books)} books into {index_name}")
