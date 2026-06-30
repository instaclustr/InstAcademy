"""Bulk-load books into bookstore-rag with classic write-throughput optimizations.

This is the canonical "fast bulk load" recipe. The steps shown here are the
exact knobs every OpenSearch operator should know about:

    Step 3: temporarily set ``refresh_interval=-1`` — Lucene stops creating new
            searchable segments during the load. Massive write speedup.
    Step 6: ``force_merge`` to a small number of segments after the load —
            fewer segments = faster searches + smaller disk footprint.
    Step 7: restore ``refresh_interval=1s`` so writes are visible quickly again.
    Step 8: ``refresh`` once to flush all the pending docs into searchable
            segments immediately.

Apply this pattern any time you load a large amount of data into an existing
index. Skip refresh tuning if the index is brand new with no concurrent reads.
"""

import json
import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

print("Step 1: Connect to OpenSearch")
client = open_search_client_from_env_file(src_env_file(__file__))
print_opensearch_connection_test(client, raise_on_error=True)

print("Step 2: Load sample-data.json")
script_dir = Path(__file__).resolve().parents[2]
sample_data_path = script_dir / "sample-data.json"
with open(sample_data_path, encoding="utf-8") as f:
    data = json.load(f)
books = data.get("results", [])
index_name = "bookstore-rag"
print(f"  Loaded {len(books)} books from {sample_data_path}")

# ``-1`` is the magic value that disables periodic refreshing entirely.
# While off, indexed docs are not searchable, but indexing throughput goes way
# up because Lucene doesn't have to roll a new segment every second.
print("Step 3: Disable index refresh during bulk (refresh_interval = -1)")
client.indices.put_settings(
    index=index_name,
    body={"index": {"refresh_interval": "-1"}},
)
print(f"  Updated settings on index {index_name!r}")

def doc_for_book(book):
    """Project a Gutendex record onto this index's field names.

    Note: this index expects ``content`` (not ``passage_text``) — different
    chapters use slightly different conventions on field names.
    """
    summaries = book.get("summaries") or []
    passage_text = summaries[0] if summaries else ""
    return {
        "id": str(book.get("id", "")),
        "title": book.get("title", ""),
        "authors": book.get("authors", []),
        "subjects": book.get("subjects", []),
        "content": passage_text,
        "bookshelves": book.get("bookshelves", []),
    }


print("Step 4: Build bulk request body")
# Each book contributes two lines: an action header + the source document.
# "NDJSON" = newline-delimited JSON, which is the over-the-wire format the
# python client builds for us.
actions = []
for book in books:
    doc = doc_for_book(book)
    actions.append({"index": {"_index": index_name, "_id": doc["id"]}})
    actions.append(doc)
print(f"  Prepared {len(books)} index operations ({len(actions)} NDJSON lines)")

print("Step 5: Run bulk index")
# Long timeout because chunking + embedding runs per doc inside the pipeline.
response = client.bulk(body=actions, request_timeout=600)
failed = [
    item
    for item in response.get("items", [])
    if "error" in item.get("index", item.get("index", {}))
]
num_failed = len(failed)
num_ok = len(books) - num_failed
if num_failed:
    print(f"  Bulk ingest: {num_ok} succeeded, {num_failed} failed")
    for item in failed[:5]:
        print("  ", item.get("index", item))
    if num_failed > 5:
        print(f"  ... and {num_failed - 5} more")
else:
    print(f"  Ingested {len(books)} books into {index_name}")

# Force merge reduces the number of Lucene segments. Fewer segments => fewer
# files to search across, smaller disk footprint, less memory for FST/doc-value
# overhead. ``max_num_segments=5`` is a sensible "post-load" value; you can
# go down to 1 for read-only indexes (slower merge, fastest searches).
print("Step 6: Force merge (max_num_segments=5)")
client.indices.forcemerge(index=index_name, max_num_segments=5)
print("  Force merge request completed")

print("Step 7: Restore refresh interval to 1s")
client.indices.put_settings(
    index=index_name,
    body={"index": {"refresh_interval": "1s"}},
)
print("  Refresh interval restored")

# Explicit refresh = "make all currently indexed docs visible now". Without
# this, docs would only become visible at the next 1s refresh tick.
print("Step 8: Refresh index so new documents are searchable")
client.indices.refresh(index=index_name)
print("  Done.")
