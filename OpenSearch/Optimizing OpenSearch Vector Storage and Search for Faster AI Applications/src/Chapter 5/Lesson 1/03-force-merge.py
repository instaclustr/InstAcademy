"""Force-merge an index to reduce Lucene segments.

Why force-merge?
    Each indexing batch creates new Lucene segments. Over time you can
    accumulate hundreds. Search performance scales with segment count (because
    every search hits every segment), and a small ``max_num_segments`` value
    reduces overhead.

When to use it:
    * After a large bulk load (one-shot reduction to a fixed target).
    * On read-only indexes (merge to 1 segment for fastest searches).

When NOT to use it:
    * During heavy write traffic — merging competes with indexing for I/O.
    * On active write indexes — Lucene's automatic merges are usually fine.

Force merge is *expensive*. It rewrites segments, which can briefly double
disk usage and saturate I/O. Run during low-traffic windows.
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
    # Targets the consolidated index built by Chapter 4 Lesson 2's
    # ``06-put-it-all-together.py``.
    index_name = "bookstore-rag-all-together"

    response = client.indices.forcemerge(
        index=index_name,
        # 5 segments is a balanced target: small enough to improve search
        # performance, large enough that the merge itself doesn't take forever.
        # For truly read-only indexes you can go to ``max_num_segments=1``.
        max_num_segments=5,
    )

    print(f"Force merge complete for index: {index_name}")
    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    main()
