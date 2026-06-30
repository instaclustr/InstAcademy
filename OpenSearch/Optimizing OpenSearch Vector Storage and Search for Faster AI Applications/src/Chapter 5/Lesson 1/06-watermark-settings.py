"""Configure cluster disk watermarks and read the current values back.

Three disk thresholds that protect a cluster from running out of disk:

    LOW (default 85%)         — when a node crosses this, OpenSearch stops
                                allocating new shards to it. Existing data
                                stays put.
    HIGH (default 90%)        — the cluster starts actively moving shards
                                off this node to others with more space.
    FLOOD_STAGE (default 95%) — last-ditch protection. All indexes with any
                                shard on the node go read-only to prevent
                                ENOSPC corruption.

Lower these on busy clusters to give yourself more reaction time. Raise them
on small lab clusters where 85% feels alarmist.
"""

import sys
from pathlib import Path

# Standard ``src/`` import path setup; see Chapter 1/Lesson 1 for full notes.
_SRC_ROOT = Path(__file__).resolve().parents[2]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from utils.opensearch_client import open_search_client_from_env_file, src_env_file

import json



def main() -> None:
    client = open_search_client_from_env_file(src_env_file(__file__))

    # ``persistent`` settings survive full cluster restart.
    response = client.cluster.put_settings(
        body={
            "persistent": {
                "cluster.routing.allocation.disk.watermark.low": "85%",
                "cluster.routing.allocation.disk.watermark.high": "90%",
                "cluster.routing.allocation.disk.watermark.flood_stage": "95%",
            }
        }
    )
    print("Updated disk watermark settings:")
    print(json.dumps(response, indent=2, default=str))

    # ``include_defaults=True`` returns built-in defaults alongside whatever you
    # explicitly set, so you can see which values are in effect even if no
    # override was applied.
    # ``flat_settings=True`` makes nested keys come back as dotted strings —
    # much easier to grep against.
    current_settings = client.cluster.get_settings(
        include_defaults=True,
        flat_settings=True,
    )
    print("\nCurrent cluster watermarks:")
    watermark_keys = (
        "cluster.routing.allocation.disk.watermark.low",
        "cluster.routing.allocation.disk.watermark.high",
        "cluster.routing.allocation.disk.watermark.flood_stage",
    )
    # Filter to just the keys we care about across all three setting scopes:
    #   persistent (survives restart), transient (cluster lifetime only),
    #   defaults (hard-coded into the build).
    filtered = {}
    for scope in ("persistent", "transient", "defaults"):
        scope_settings = current_settings.get(scope, {})
        filtered[scope] = {
            key: scope_settings[key] for key in watermark_keys if key in scope_settings
        }
    print(json.dumps(filtered, indent=2, default=str))


if __name__ == "__main__":
    main()
