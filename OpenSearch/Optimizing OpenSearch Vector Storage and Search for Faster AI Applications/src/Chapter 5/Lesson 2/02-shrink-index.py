"""Demonstrate the full "shrink an index" workflow with an alias swap.

What is index shrinking?
    Re-creates the source index with **fewer primary shards** (the target's
    primary count must be a factor of the source's). Useful when you've
    over-sharded a time-series index that's gone read-only, or you want to
    reduce per-shard overhead after a write phase ends.

Six-step recipe (this is the canonical recipe — memorize it):
    1. Move all shards to a single node and block writes. Shrink needs all
       primaries co-located on one node.
    2. ``_shrink`` to the target name with the desired shard / replica /
       codec settings.
    3. Remove the allocation-require setting from the new index so it can
       balance freely.
    4. ``force_merge`` the shrunk index to one segment (rare case where 1 is
       the right answer — the new index is supposed to be smaller and static).
    5. Swap the alias from old -> new in a single atomic operation so reads
       never see "no index here".
    6. Delete the original index to reclaim space.
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
    source_index = "bookstore-rag-all-together"
    target_index = "bookstore-rag-all-together-shrunk"
    # Alias is what clients use; the alias swap is the bit that makes this
    # whole dance invisible to callers.
    alias_name = "bookstore-rag-all-together-alias"

    # Step 1: pin every shard onto ``node-1`` and block writes. Both are
    # preconditions for ``_shrink`` — all primaries must be on one node and
    # the source index must not accept new docs during the operation.
    step1 = client.indices.put_settings(
        index=source_index,
        body={
            "settings": {
                # Require allocation only on the named node.
                "index.routing.allocation.require._name": "node-1",
                # Hard write block — index becomes read-only.
                "index.blocks.write": True,
            }
        },
    )
    print("Step 1: move shards and block writes")
    print(json.dumps(step1, indent=2, default=str))

    # Step 2: do the shrink. Target gets:
    #   number_of_shards=1     -- the whole point of shrinking
    #   number_of_replicas=1   -- restore HA on the new index
    #   codec=best_compression -- since this index is now mostly read-only,
    #                              optimize for disk footprint over CPU
    step2 = client.indices.shrink(
        index=source_index,
        target=target_index,
        body={
            "settings": {
                "index.number_of_shards": 1,
                "index.number_of_replicas": 1,
                "index.codec": "best_compression",
            }
        },
    )
    print("\nStep 2: shrink index")
    print(json.dumps(step2, indent=2, default=str))

    # Step 3: clear the routing requirement so the new index can rebalance
    # to other nodes for HA. Setting a value to None removes the setting.
    step3 = client.indices.put_settings(
        index=target_index,
        body={"index.routing.allocation.require._name": None},
    )
    print("\nStep 3: remove routing requirement")
    print(json.dumps(step3, indent=2, default=str))

    # Step 4: collapse to one segment for fastest searches. Safe here because
    # the new index is read-only-by-design (data won't change).
    step4 = client.indices.forcemerge(index=target_index, max_num_segments=1)
    print("\nStep 4: force merge")
    print(json.dumps(step4, indent=2, default=str))

    # Step 5: atomic alias swap. ``update_aliases`` applies all actions in a
    # single cluster state update, so there is no instant where neither index
    # owns the alias. Clients querying the alias see a seamless transition.
    step5 = client.indices.update_aliases(
        body={
            "actions": [
                {"remove": {"index": source_index, "alias": alias_name}},
                {"add": {"index": target_index, "alias": alias_name}},
            ]
        }
    )
    print("\nStep 5: alias swap")
    print(json.dumps(step5, indent=2, default=str))

    # Step 6: drop the original, now that nothing reads from it via the alias.
    step6 = client.indices.delete(index=source_index)
    print("\nStep 6: delete old index")
    print(json.dumps(step6, indent=2, default=str))

    # Quick sanity check — the source should be empty (deleted), and the
    # target should have far fewer shards listed.
    print("\nShard counts:")
    before = client.cat.shards(index=source_index, params={"v": "true"}, format="json")
    after = client.cat.shards(index=target_index, params={"v": "true"}, format="json")
    print(f"- {source_index}: {len(before)} shard rows")
    print(f"- {target_index}: {len(after)} shard rows")


if __name__ == "__main__":
    main()
