"""Inspect shard distribution across nodes — verifies allocation health.

Why look at this?
    After tweaking routing awareness, allocation enable/disable, or replica
    counts, you want to confirm shards actually moved. ``_cat/shards`` with
    ``sort by node`` gives you a per-node grouping so you can see:

      * Whether each node has roughly the same count of primaries + replicas.
      * Whether any shards are stuck in ``UNASSIGNED`` / ``INITIALIZING``.
      * Whether primary + replica of the same shard ended up on different nodes.
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

    # ``s=node`` sorts the cat output by node name so you can scan one node at a time.
    # ``v=true`` keeps the column headers visible (only really visible in text format).
    shards = client.cat.shards(
        params={"v": "true", "s": "node"},
        format="json",
    )

    print("Shard distribution (sorted by node):")
    print(json.dumps(shards, indent=2, default=str))


if __name__ == "__main__":
    main()
