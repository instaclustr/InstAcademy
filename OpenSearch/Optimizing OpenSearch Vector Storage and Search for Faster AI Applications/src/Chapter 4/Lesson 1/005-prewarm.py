"""k-NN plugin: warmup an index, read stats, and set the memory circuit breaker.

What this script teaches:
    * **Warmup**: the k-NN plugin keeps HNSW graphs in native (off-heap) memory.
      The first query to each shard triggers a graph load (slow). Calling
      ``/_plugins/_knn/warmup/{index}`` pre-loads them so the first user-facing
      query is already fast.
    * **k-NN stats**: per-node counters for graph memory usage, cache hit rate,
      etc. — your main signal that vector search is healthy.
    * **Memory circuit breaker**: caps how much native memory the plugin will
      grab before refusing new graph loads. Prevents the k-NN cache from
      eating the whole machine.

Mirrors these Dev Tools requests::

    GET /_plugins/_knn/warmup/<index>
    GET /_plugins/_knn/stats
    PUT /_cluster/settings (persistent knn.memory.circuit_breaker.limit)
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file

import json
import os


client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

index_name = os.environ.get("BOOKSTORE_RAG_INDEX", "bookstore-rag-index")
# Default 60% of available native memory — leave headroom for the OS and JVM.
breaker_limit = os.environ.get("KNN_MEMORY_CIRCUIT_BREAKER_LIMIT", "60%")

print(f"\n--- k-NN warmup: {index_name} ---")
# Loads HNSW graphs for every shard of ``index_name`` into the native cache.
# Cheap to call repeatedly — already-loaded shards just become no-ops.
warmup = client.transport.perform_request(
    "GET",
    f"/_plugins/_knn/warmup/{index_name}",
)
print(json.dumps(warmup, indent=2, default=str))

print("\n--- k-NN stats ---")
# Returns one block of stats per node. Useful fields:
#   graph_memory_usage_percentage  -- how full the cache is
#   cache_hit_rate                 -- 1.0 = every query found its graph in cache
#   graph_query_requests           -- total queries served
stats = client.transport.perform_request("GET", "/_plugins/_knn/stats")
print(json.dumps(stats, indent=2, default=str))

print(f"\n--- cluster settings: knn.memory.circuit_breaker.limit = {breaker_limit} ---")
# When usage exceeds this percentage, the plugin starts evicting LRU graphs.
# Setting it too low causes constant re-loads; too high risks OS-level OOM.
settings_resp = client.cluster.put_settings(
    body={"persistent": {"knn.memory.circuit_breaker.limit": breaker_limit}},
)
print(json.dumps(settings_resp, indent=2, default=str))
