"""Inspect cluster health, fix replica count, and learn the allocation-explain API.

This script demonstrates how to diagnose and fix the kind of issue the
previous script (``04-index-too-many-shards.py``) deliberately created:

    1. Print health before — likely YELLOW because replicas can't be allocated.
    2. Reduce ``number_of_replicas`` to 0, freeing the replica shards.
    3. Print health after — should be GREEN.
    4. Print shard details + allocation overview for context.
    5. Call ``_cluster/allocation/explain`` — the API for "why is THIS shard
       unassigned?". The single most useful debugging tool when shards are
       stuck.
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
    index_name = "my-index"

    # Cluster health summary: status (green/yellow/red), shard counts,
    # number of unassigned shards. Run this often when debugging.
    health_before = client.cluster.health()
    print("Cluster health (before replica update):")
    print(json.dumps(health_before, indent=2, default=str))

    # Set replicas to 0 — every shard becomes a primary only. On a single-node
    # cluster this is the fix for yellow status caused by un-assignable replicas.
    # On a multi-node prod cluster you'd usually keep at least 1 replica for HA.
    put_settings_response = client.indices.put_settings(
        index=index_name,
        body={"number_of_replicas": 0},
    )
    print("\nUpdated replica settings:")
    print(json.dumps(put_settings_response, indent=2, default=str))

    health_after = client.cluster.health()
    print("\nCluster health (after replica update):")
    print(json.dumps(health_after, indent=2, default=str))

    # Per-shard details. ``unassigned.reason`` is the killer column — it tells
    # you why a shard is stuck (CLUSTER_RECOVERED, NODE_LEFT, ALLOCATION_FAILED, ...).
    shards = client.cat.shards(
        params={"v": "true", "h": "index,shard,prirep,state,node,unassigned.reason"},
        format="json",
    )
    print("\nShard details:")
    print(json.dumps(shards, indent=2, default=str))

    # Per-node disk usage — needed to spot watermark issues (next script).
    allocation = client.cat.allocation(
        params={"v": "true", "h": "node,disk.used_percent,disk.avail"},
        format="json",
    )
    print("\nAllocation overview:")
    print(json.dumps(allocation, indent=2, default=str))

    # ``allocation/explain`` is the diagnostic API for shard placement.
    # Given a (index, shard, primary?) tuple, it tells you exactly why every
    # node was or wasn't picked as a destination. Indispensable when shards
    # refuse to allocate and ``_cat/shards`` only says "ALLOCATION_FAILED".
    allocation_explain = client.transport.perform_request(
        "GET",
        "/_cluster/allocation/explain",
        body={
            "index": index_name,
            "shard": 1,
            "primary": True,
        },
    )
    print("\nAllocation explain:")
    print(json.dumps(allocation_explain, indent=2, default=str))

if __name__ == "__main__":
    main()
