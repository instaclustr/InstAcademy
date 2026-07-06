"""Load sample-data.json and bulk-ingest each book into my-sparse-neural-index.

Because that index has ``nlp-ingest-pipeline`` attached as ``default_pipeline``,
each ``passage_text`` value gets:
    1. Chunked into small token windows.
    2. Encoded into per-chunk sparse vectors (rank_features).

That ingest work is invisible to the client — we just write JSON.
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

# sample-data.json lives at src/sample-data.json (one level up).
sample_data_path = _SRC_ROOT / "sample-data.json"
with open(sample_data_path, encoding="utf-8") as f:
    data = json.load(f)

books = data.get("results", [])
index_name = "my-sparse-neural-index"


def doc_for_book(book):
    """Trim a Gutendex record down to the fields our index uses."""
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

# request_timeout=600 (10 min): sparse encoding through chunking runs the model
# once per chunk per doc, so bulk is slower than a plain index.
response = client.bulk(body=actions, request_timeout=600)
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

client.indices.refresh(index=index_name)
print(f"Refreshed {index_name}")
