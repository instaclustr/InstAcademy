"""Configure OpenSearch search backpressure to protect the cluster from expensive queries.

What is "search backpressure"?
    A built-in mechanism that **cancels in-flight searches** when a node is
    under stress, prioritizing cluster stability over individual queries
    completing. Modes:
        enforced     — actively cancel offending tasks
        monitor_only — track the same signals, log, but don't cancel
        disabled     — off

It looks at two scopes:
    * ``search_task`` — coordinator-level work (the top-level search request).
    * ``search_shard_task`` — per-shard sub-tasks.

For each scope you can configure CPU time, elapsed time, heap usage thresholds
plus a cancellation **rate** and **burst** so you don't cancel everything in
one second.

This script is "monitor_only" so you can observe what *would* be cancelled
in your environment before flipping to enforced.
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

    # Round 1: thresholds. These say "what counts as expensive".
    thresholds_response = client.cluster.put_settings(
        body={
            "persistent": {
                # Observe-only mode — log candidates without cancelling.
                # Use ``enforced`` once you trust the thresholds in production.
                "search_backpressure.mode": "monitor_only",
                # Per-shard task spending more than 30s of CPU is "expensive".
                "search_backpressure.search_shard_task.cpu_time_millis_threshold": 30000,
                # Per-shard task running longer than 45s wall-clock is "expensive".
                "search_backpressure.search_shard_task.elapsed_time_millis_threshold": 45000,
                # A coordinator-level task that has accumulated >5% of total JVM heap
                # in result buffers is "expensive".
                "search_backpressure.search_task.total_heap_percent_threshold": 0.05,
                # "Node duress" triggers — backpressure activates only when the
                # node itself is unhealthy. Cancelling slow queries on a healthy
                # node is unnecessary.
                "search_backpressure.node_duress.cpu_threshold": 0.90,
                "search_backpressure.node_duress.heap_threshold": 0.70,
            }
        }
    )
    print("Applied search backpressure thresholds:")
    print(json.dumps(thresholds_response, indent=2, default=str))

    # Round 2: cancellation rate-limiting. These prevent a thundering herd of
    # cancellations from itself causing problems.
    cancellation_response = client.cluster.put_settings(
        body={
            "persistent": {
                # 5% rate = up to 5% of running tasks can be cancelled per second.
                "search_backpressure.search_task.cancellation_rate": 0.05,
                # Burst = the max bucket size of the rate-limiter — extra
                # cancellations allowed in a brief spike before the rate kicks in.
                "search_backpressure.search_task.cancellation_burst": 10,
                # Same knobs for per-shard scope (typically more cancellations
                # allowed because each search yields several shard tasks).
                "search_backpressure.search_shard_task.cancellation_rate": 0.05,
                "search_backpressure.search_shard_task.cancellation_burst": 15,
            }
        }
    )
    print("\nApplied cancellation settings:")
    print(json.dumps(cancellation_response, indent=2, default=str))

    # Stats endpoint shows current backpressure state per node — useful for
    # confirming "monitor_only" is actually triggering on your traffic.
    stats_response = client.transport.perform_request("GET", "/_nodes/stats/search_backpressure")
    print("\nSearch backpressure stats:")
    print(json.dumps(stats_response, indent=2, default=str))


if __name__ == "__main__":
    main()
