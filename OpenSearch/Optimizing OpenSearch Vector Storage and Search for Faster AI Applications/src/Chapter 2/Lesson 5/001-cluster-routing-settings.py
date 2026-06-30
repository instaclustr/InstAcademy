"""Set OpenSearch cluster routing settings (allocation and rebalance).

What these settings do:
    * ``cluster.routing.allocation.enable`` — controls *whether* the cluster
      is allowed to allocate shards to nodes. Useful to set to ``none`` before
      doing a rolling restart so the cluster doesn't start moving data around.
    * ``cluster.routing.rebalance.enable`` — controls *whether* the cluster is
      allowed to move shards between nodes to keep things balanced.

For day-to-day operation both should be ``all``. They become interesting during
maintenance: temporarily disabling rebalancing while you take a node out for a
restart prevents wasted shard movements.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/1-1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, print_opensearch_connection_test, src_env_file



# Configure your OpenSearch connection.
client = open_search_client_from_env_file(src_env_file(__file__))

print_opensearch_connection_test(client, raise_on_error=True)

# PUT /_cluster/settings
# Allowed values:
#   allocation.enable: all | primaries | new_primaries | none
#   rebalance.enable:  all | primaries | replicas | none
#   allow_rebalance (optional): always | indices_primaries_active | indices_all_active
#
# Using ``persistent`` (survives full cluster restart) instead of ``transient``
# (lost on full restart) is the safer default for permanent operational settings.
persistent = {
    "cluster.routing.allocation.enable": "all",
    "cluster.routing.rebalance.enable": "all",
    # Commented out — the default is fine for most clusters. Uncomment to only
    # rebalance once every index's shards are active.
    # "cluster.routing.allocation.allow_rebalance": "indices_all_active",
}

response = client.cluster.put_settings(body={"persistent": persistent})
# ``acknowledged`` = master accepted the update. For cluster settings that's
# the only confirmation you get — propagation to other nodes is implicit.
if response.get("acknowledged"):
    print("Cluster routing settings updated:")
    for key, value in persistent.items():
        print(f"  {key} = {value}")
else:
    print("Response:", response)
