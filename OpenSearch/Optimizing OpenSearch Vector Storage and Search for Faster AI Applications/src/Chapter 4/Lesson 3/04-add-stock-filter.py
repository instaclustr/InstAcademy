"""Wire a search pipeline up as the *default* search pipeline for an index.

What ``index.search.default_pipeline`` does:
    Once set, **every** search against that index is automatically routed
    through the named pipeline — without callers having to pass
    ``?search_pipeline=...``. Great for enforcing things like a stock filter
    or score boost across the whole app.

The flip side: a default pipeline applies to *all* queries on the index, which
can be surprising. Use ``?search_pipeline=_none`` on a request to bypass it.
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
    index_name = "bookstore-rag"
    # Pipeline id from a *previous* lesson script. Make sure it exists before
    # running this — otherwise queries will start failing once the default is set.
    pipeline_id = "bookstore-stock-filter"

    # Index-level setting (note: ``index.search.default_pipeline``, different
    # from ``index.default_pipeline`` which is the ingest pipeline).
    response = client.indices.put_settings(
        index=index_name,
        body={"index.search.default_pipeline": pipeline_id},
    )

    print(f"Updated index settings for: {index_name}")
    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    main()
