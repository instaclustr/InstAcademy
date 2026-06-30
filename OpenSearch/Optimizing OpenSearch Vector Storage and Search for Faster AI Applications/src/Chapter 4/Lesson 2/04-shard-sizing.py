"""Inspect shard sizes and learn the rules of thumb for ``number_of_shards``.

This script doesn't change anything — it just reads ``_cat/shards`` and prints
per-shard doc counts and store size. Watching this number grow as you ingest
helps you decide if you need more shards for the next iteration of the index.

Shard sizing rules of thumb (heuristics, not laws):
    number_of_shards = total_data_size_GB / target_shard_size_GB
    Example: 100GB / 10GB = 10 shards

Target shard size depends on workload:
    For search-heavy RAG: target 10–30 GB per shard
    For write-heavy:      target 30–50 GB per shard
    For pure vector:      start at 50 GB, reduce to as little as 10 GB if
                          hybrid + latency sensitive

Why care?
    Tiny shards = too much per-query coordination overhead.
    Huge shards = slow recovery, slow rebalance, hot nodes, OOM risk.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

import json


client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# ``_cat`` APIs return either text tables or JSON. ``format="json"`` makes
# Python parsing trivial. The ``h=`` parameter selects which columns to return.
#   index, shard, prirep (p=primary, r=replica), state, docs (doc count),
#   store (size on disk, human-readable like "4.8gb").
shards = client.cat.shards(
    index="bookstore-rag",
    params={"v": "true", "h": "index,shard,prirep,state,docs,store"},
    format="json",
)

if not shards:
    print("No shard data found for index 'bookstore-rag'.")
else:
    # Render as a simple tab-separated table for quick eyeballing.
    print("index\tshard\tprirep\tstate\tdocs\tstore")
    for row in shards:
        print(
            f"{row.get('index', '')}\t"
            f"{row.get('shard', '')}\t"
            f"{row.get('prirep', '')}\t"
            f"{row.get('state', '')}\t"
            f"{row.get('docs', '')}\t"
            f"{row.get('store', '')}"
        )

# Example of what a healthy row looks like:
# index          shard prirep state   docs  store
# bookstore-rag  0     p      STARTED  500k  4.8gb
