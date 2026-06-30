"""Warm the k-NN cache and configure file-level preload for vector search.

Two layers of "make first queries fast":
    1. ``_plugins/_knn/warmup/{index}`` — load HNSW graphs into the k-NN
       plugin's native memory. Until you call this (or someone queries each
       shard once), the first query per shard pays a graph-load cost.
    2. ``index.store.preload`` — tell Lucene to ``mmap`` certain file
       extensions into the OS page cache when an index opens. Lower-level
       than #1 but cheaper to maintain.

Why does ``index.store.preload`` need a close/open?
    It's a **non-dynamic** setting — the changes only take effect when an
    index is opened. So we close the index, change the setting, and reopen.
    Cluster health goes red briefly during the close.
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

# Warm the k-NN index — loads HNSW graphs into native memory.
index_name = "bookstore-rag"
warmup_response = client.transport.perform_request(
    method="GET",
    url=f"/_plugins/_knn/warmup/{index_name}",
)
print("Warmup response:")
print(json.dumps(warmup_response, indent=2))

# Response shows how many shards were warmed:
# { "_shards": { "total": 2, "successful": 2, "failed": 0 } }

# Native memory accounting after warming — useful to confirm graphs are loaded.
stats_response = client.transport.perform_request(
    method="GET",
    url="/_plugins/_knn/stats",
)
print("k-NN stats:")
# Stats are per-node. For a single-node lab, grabbing the first entry is fine.
# In production you'd iterate every node to confirm the warm spread.
nodes_stats = stats_response.get("nodes", {})
first_node_stats = next(iter(nodes_stats.values()), {})
graph_memory_usage_percentage = first_node_stats.get("graph_memory_usage_percentage", "N/A")
cache_hit_rate = first_node_stats.get("cache_hit_rate", "N/A")
graph_query_requests = first_node_stats.get("graph_query_requests", "N/A")
print(f"graph_memory_usage_percentage: {graph_memory_usage_percentage}")
print(f"cache_hit_rate: {cache_hit_rate}")
print(f"graph_query_requests: {graph_query_requests}")

# Key stats to look at in the response:
# "graph_memory_usage_percentage"  -- how much of the circuit breaker limit is used
# "cache_hit_rate"                 -- should rise toward 1.0 after warming
# "graph_query_requests"           -- total graph queries served

# index.store.preload is non-dynamic; close index before updating it.
# Closing an index makes it unavailable for read/write but keeps the data on
# disk. Necessary because some Lucene settings can only be applied on open.
close_response = client.indices.close(index=index_name)
print("Close index response:")
print(json.dumps(close_response, indent=2))

try:
    # ``vec`` = k-NN vectors, ``vem`` = vector metadata. Pre-touching these
    # extensions warms the OS page cache for faster first queries after open.
    preload_response = client.indices.put_settings(
        index=index_name,
        body={
            "index": {
                "store": {
                    "preload": ["vec", "vem"],
                }
            }
        },
    )
    print("Preload setting response:")
    print(json.dumps(preload_response, indent=2))
finally:
    # ``try/finally`` so a failure in put_settings doesn't leave the index closed.
    open_response = client.indices.open(index=index_name)
    print("Open index response:")
    print(json.dumps(open_response, indent=2))

# After reopen, wait for at least yellow status (primary shards ready).
# Without this, the next script could see a still-recovering index.
health_response = client.cluster.health(index=index_name, wait_for_status="yellow", timeout=60)
print("Index health after reopen:")
print(json.dumps(health_response, indent=2))
