"""Configure cluster routing awareness so OpenSearch spreads shards across zones.

What is "routing awareness"?
    OpenSearch's shard allocator normally just balances by count + disk usage.
    With awareness on, it also tries to *not* put a primary and its replica
    on nodes that share an attribute (like the same availability zone or rack).

    Pair it with ``force.<attribute>.values`` to **forbid** allocating shards
    if some zone isn't represented — useful for multi-AZ clusters where you
    never want all replicas of one shard ending up in a single zone.

Prerequisite:
    Each node must expose its zone attribute via ``node.attr.zone=zoneN`` in
    its opensearch.yml. Without that, this setting does nothing.
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

    response = client.cluster.put_settings(
        body={
            "persistent": {
                # Comma-separated list of attribute names to use for awareness.
                # Here just "zone", but you could have multiple (rack, zone, ...).
                "cluster.routing.allocation.awareness.attributes": "zone",
                # Force-aware: shards refuse to allocate until at least one node
                # is up in each listed zone. Stops a partial cluster from
                # silently piling all replicas into the surviving zone.
                "cluster.routing.allocation.awareness.force.zone.values": "zone1,zone2,zone3",
            }
        }
    )

    print("Updated cluster routing awareness settings")
    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    main()
