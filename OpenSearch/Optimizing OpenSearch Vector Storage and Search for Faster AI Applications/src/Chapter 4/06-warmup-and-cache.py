"""Chapter 4 · Step 13 — warm the k-NN cache, read stats, and tune the circuit breaker."""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

client = open_search_client_from_env_file(_SRC / ".env")
print_opensearch_connection_test(client, raise_on_error=True)

warm = client.transport.perform_request("GET", "/_plugins/_knn/warmup/bookstore-rag-index")
print("Warmup:", warm)

stats = client.transport.perform_request("GET", "/_plugins/_knn/stats")
# Print a couple of headline node stats if present.
nodes = stats.get("nodes", {})
for node_id, s in list(nodes.items())[:1]:
    print("graph_memory_usage_percentage:", s.get("graph_memory_usage_percentage"))
    print("cache_hit_rate:", s.get("cache_hit_rate"))
    print("graph_query_requests:", s.get("graph_query_requests"))

client.cluster.put_settings(body={"persistent": {"knn.memory.circuit_breaker.limit": "60%"}})
print("Set knn.memory.circuit_breaker.limit = 60%")
