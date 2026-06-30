"""Create ``my-index`` with intentionally too many shards (to demo what *not* to do).

This is a teaching example for "oversharding":
    * 6 primaries x 1 replica = 12 shards total.
    * For a tiny dataset, that's *way* too many — overhead per shard dominates,
      and the cluster may not even have enough nodes to spread them.

The next script in this lesson uses this index to demonstrate cluster health
going yellow/red, then walks you through fixing it by adjusting replicas.

Real-world advice:
    Start with fewer shards and grow if needed. Pick shard count using the
    rule of thumb from ``Chapter 4 Lesson 2 / 04-shard-sizing.py``: target
    10–50 GB per shard depending on workload.
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
    index_name = "my-index"

    # Re-create on every run so the demo is reproducible. (You generally do
    # NOT do this on real indexes — deleting wipes all data.)
    if client.indices.exists(index=index_name):
        print(f"Index '{index_name}' already exists. Deleting it first.")
        client.indices.delete(index=index_name)

    response = client.indices.create(
        index=index_name,
        body={
            "settings": {
                # 6 primaries on a probably-small cluster — deliberately too many.
                "number_of_shards": 6,
                # 1 replica per primary, so 12 total shards. On a 2-node cluster
                # this leaves replicas un-allocatable (a node can't host both
                # primary and its replica) → yellow status.
                "number_of_replicas": 1,
            }
        },
    )

    print(f"Created index: {index_name}")
    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    main()
