"""Reindex ``my-index`` -> ``my-index-new`` with a Painless script that merges fields.

What ``_reindex`` is for:
    Server-side bulk copy from one index to another. Often used to:
        * Apply a new mapping that's incompatible with the old one.
        * Migrate to a different shard count / engine without downtime.
        * Apply transformations to every document in flight.

The transformation here merges ``author`` into ``title`` and drops the
``author`` field. Trivial as a demo — but the pattern (mutate ``ctx._source``,
optionally call ``ctx.op = 'noop'`` or ``'delete'`` to skip docs) is the
foundation of every real reindex you'll ever write.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see src/Chapter 1 scripts for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file

import json



def main() -> None:
    client = open_search_client_from_env_file(_SRC_ROOT / ".env")
    response = client.reindex(
        body={
            "source": {"index": "my-index"},
            # ``my-index-new`` must already exist (or be auto-creatable) before
            # reindex starts. In a real workflow you'd PUT the new mapping first.
            "dest": {"index": "my-index-new"},
            "script": {
                # Painless script runs once per source document.
                # ``ctx._source`` is the document body — mutate in place.
                "source": """
                ctx._source.title = ctx._source.title + ' ' + ctx._source.author;
                ctx._source.remove('author');
                """,
                "lang": "painless",
            },
        },
        params={
            # ``slices=5`` parallelizes the reindex across 5 internal sub-tasks.
            # Roughly: number_of_shards is a sensible upper bound. Speeds up
            # large reindexes dramatically.
            "slices": 5,
            # Block this client call until reindex finishes. For very large
            # reindexes set ``"false"`` and poll the ``_tasks`` API instead.
            "wait_for_completion": "true",
        },
    )
    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    main()
