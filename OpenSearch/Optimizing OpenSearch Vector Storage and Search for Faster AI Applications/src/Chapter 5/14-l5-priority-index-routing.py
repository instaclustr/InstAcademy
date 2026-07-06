"""Route different indexes to different node tiers with ``allocation.require``.

Pattern: tiered hardware
    Imagine a cluster with two flavours of node:
        * "power"    — fast CPU + lots of RAM, expensive.
        * "standard" — modest CPU + RAM, cheap.

    Each node tags itself in opensearch.yml:
        node.attr.node_type: power     # or "standard"

    You can then *require* each index to land only on nodes with the matching
    tag. That's how you keep critical indexes (like ``orders``) on the fast
    tier and bulk/browseable data (like ``book-browse``) on the cheap tier.

The setting used here, ``index.routing.allocation.require.<attr>``, means
"only allocate shards for this index on nodes where the attribute equals X".
Related options: ``include`` (any of), ``exclude`` (none of).
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see src/Chapter 1 scripts for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file

import json



def ensure_index(client: object, index_name: str) -> None:
    """Create the index only if it doesn't exist. Idempotent ``mkdir -p``-style helper."""
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name)


def main() -> None:
    client = open_search_client_from_env_file(_SRC_ROOT / ".env")

    # Two demo indexes with very different priorities.
    orders_index = "orders"
    browse_index = "book-browse"
    ensure_index(client, orders_index)
    ensure_index(client, browse_index)

    # Pin ``orders`` to the high-end "power" tier — latency-sensitive, expensive
    # to lose data, deserves the best hardware.
    orders_response = client.indices.put_settings(
        index=orders_index,
        body={"index.routing.allocation.require.node_type": "power"},
    )
    print(f"Updated routing for {orders_index}:")
    print(json.dumps(orders_response, indent=2, default=str))

    # Pin ``book-browse`` to commodity "standard" nodes — large dataset, low
    # update rate, traffic is bursty but tolerant of higher latency.
    browse_response = client.indices.put_settings(
        index=browse_index,
        body={"index.routing.allocation.require.node_type": "standard"},
    )
    print(f"\nUpdated routing for {browse_index}:")
    print(json.dumps(browse_response, indent=2, default=str))


if __name__ == "__main__":
    main()
