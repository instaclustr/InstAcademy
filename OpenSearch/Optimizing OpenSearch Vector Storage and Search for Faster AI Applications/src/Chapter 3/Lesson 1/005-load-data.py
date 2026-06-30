"""Load sample-data.json and bulk-ingest each book into my-sparse-neural-index.

Same shape as Chapter 2's data loader, but pointed at the **sparse** index.
Because that index has the ``nlp-ingest-pipeline`` attached as
``default_pipeline``, each ``passage_text`` value gets:
    1. Chunked into small token windows.
    2. Encoded into per-chunk sparse vectors (rank_features).

That ingest work is invisible to the client — we just write JSON.
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

# Load sample-data.json from ``src/sample-data.json``.
script_dir = Path(__file__).resolve().parents[2]
sample_data_path = script_dir / "sample-data.json"
with open(sample_data_path, encoding="utf-8") as f:
    data = json.load(f)

books = data.get("results", [])
index_name = "my-sparse-neural-index"

def doc_for_book(book):
    """Trim a Gutendex record down to the fields our index uses.

    Same helper as Chapter 2's loader — kept inline (not factored to ``utils``)
    so each lesson is self-contained for reading.
    """
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

actions = []
for book in books:
    doc = doc_for_book(book)
    actions.append({"index": {"_index": index_name, "_id": doc["id"]}})
    actions.append(doc)

# ``request_timeout=600`` (10 min) — sparse encoding through chunking is
# slower than dense embedding because the model runs once per chunk per doc.
# For dozens of books with a few chunks each, a few minutes is reasonable.
response = client.bulk(body=actions, request_timeout=600)
failed = [
    item
    for item in response.get("items", [])
    if "error" in item.get("index", item.get("index", {}))
]
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
