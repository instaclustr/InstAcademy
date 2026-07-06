"""Configure cluster routing awareness so OpenSearch spreads shards across zones.

What is "routing awareness"?
    OpenSearch's shard allocator normally just balances by count + disk usage.
    With awareness on, it also tries to *not* put a primary and its replica
    on nodes that share an attribute (like the same availability zone or rack).

    Pair it with ``force.<attribute>.values`` to **forbid** allocating shards
    if some zone isn't represented — useful for multi-AZ clusters where you
    never want all replicas of one shard ending up in a single zone.

Prerequisite:
    Each node must expose its zone attribute via ``node.attr.<attribute>=...`` in
    its opensearch.yml. Without that, this setting does nothing.

    On the Instaclustr trial cluster, nodes do not set ``node.attr.zone`` --
    check ``GET _nodes?filter_path=nodes.*.attributes`` first. Instaclustr
    nodes advertise ``node.attr.rack_id`` (one AWS AZ per rack, e.g.
    "us-west-2a"), so this script uses that real attribute instead of the
    fictitious "zone" so the awareness setting actually has an effect
    (verified live: the cluster stayed green with 100% active shards).
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

    response = client.cluster.put_settings(
        body={
            "persistent": {
                # Comma-separated list of attribute names to use for awareness.
                # Here just "rack_id" (Instaclustr's real per-node attribute),
                # but you could have multiple (rack, zone, ...).
                "cluster.routing.allocation.awareness.attributes": "rack_id",
                # Force-aware: shards refuse to allocate until at least one node
                # is up in each listed zone. Stops a partial cluster from
                # silently piling all replicas into the surviving zone.
                "cluster.routing.allocation.awareness.force.rack_id.values": "us-west-2a,us-west-2b,us-west-2c",
            }
        }
    )

    print("Updated cluster routing awareness settings")
    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    main()
