"""Chapter 4 · Steps 18-19 — inspect shard sizes, warm k-NN, and preload vector files.

index.store.preload takes effect on index open, so the sequence is close -> set -> open.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test

client = open_search_client_from_env_file(_SRC / ".env")
print_opensearch_connection_test(client, raise_on_error=True)

# Step 18: shard sizes. Target 10-30 GB/shard for search-heavy RAG.
shards = client.cat.shards(index="bookstore-rag", params={"v": "true", "h": "index,shard,prirep,state,docs,store"})
print(shards)

# Step 19: warm then preload vec/vem.
print("Warmup:", client.transport.perform_request("GET", "/_plugins/_knn/warmup/bookstore-rag"))
client.indices.close(index="bookstore-rag")
client.indices.put_settings(index="bookstore-rag", body={"index": {"store": {"preload": ["vec", "vem"]}}})
client.indices.open(index="bookstore-rag")
health = client.cluster.health(index="bookstore-rag", params={"wait_for_status": "yellow", "timeout": "60s"})
print("Health:", health.get("status"))
