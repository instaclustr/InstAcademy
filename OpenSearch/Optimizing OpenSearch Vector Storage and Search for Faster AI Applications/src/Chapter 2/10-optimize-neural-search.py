"""Lesson 2-5: apply neural-search optimizations across cluster and index layers.

Covers the runnable settings from the lesson:
    * Cluster: the k-NN native-memory circuit breaker (protects nodes from OOM).
    * Cluster: shard routing allocation/rebalance (stable placement for ANN graphs).
    * Index:   refresh interval (fewer, larger segments = faster ANN traversal)
               and ef_search (ANN candidate-list size = recall/latency tradeoff).

Shard sizing, replicas, on_disk mode, dimensionality, and query batching are
design decisions covered in the README rather than one-shot API calls.
"""

import sys
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from opensearchpy.exceptions import TransportError  # type: ignore[import-untyped]

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

_ENV_FILE = _SRC_ROOT / ".env"
INDEX = "vector-search-index"

client = open_search_client_from_env_file(_ENV_FILE)
print_opensearch_connection_test(client, raise_on_error=True)

# --- Cluster layer -------------------------------------------------------------
# k-NN native-memory circuit breaker: caps native memory for ANN graphs and
# evicts least-recently-used graphs before a node OOMs. Default limit is 50%.
# Routing: for day-to-day operation both knobs are ``all``; operators set
# allocation.enable=none before a rolling restart to avoid churning ANN graphs.
cluster_persistent = {
    "knn.memory.circuit_breaker.enabled": True,
    "knn.memory.circuit_breaker.limit": "50%",
    "cluster.routing.allocation.enable": "all",
    "cluster.routing.rebalance.enable": "all",
    # Uncomment to rebalance only after every index's shards are active:
    # "cluster.routing.allocation.allow_rebalance": "indices_all_active",
}
resp = client.cluster.put_settings(body={"persistent": cluster_persistent})
if resp.get("acknowledged"):
    print("Cluster settings updated:")
    for k, v in cluster_persistent.items():
        print(f"  {k} = {v}")

# --- Index layer ---------------------------------------------------------------
# Raise the refresh interval during heavy ingest to reduce tiny-segment churn,
# and set ef_search (dynamic ANN candidate list; higher = better recall, slower).
try:
    client.indices.put_settings(
        index=INDEX,
        body={
            "index.refresh_interval": "30s",
            "index.knn.algo_param.ef_search": 100,
        },
    )
    print(f"Index settings updated on {INDEX}: refresh_interval=30s, ef_search=100")
    # After heavy ingest, consolidate segments so the k-NN graph lives in fewer,
    # larger segments (faster traversal). Can take a while on large indexes.
    client.indices.forcemerge(index=INDEX, max_num_segments=1)
    print(f"Force-merged {INDEX} to 1 segment per shard")
except TransportError as exc:
    if getattr(exc, "status_code", None) == 404:
        print(f"Index {INDEX} not found — run 06-create-index.py and 07-ingest-data.py first.")
    else:
        raise
