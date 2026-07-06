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

Prerequisite fix (found on the real cluster):
    ``_shrink`` requires the source to have MORE THAN ONE primary shard.
    Chapter 4 · Lesson 4-2 builds ``bookstore-rag`` without an explicit
    ``number_of_shards``, which defaults to 1 -- verified live, the shrink
    call fails with ``illegal_argument_exception: can't shrink an index
    with only one shard``. This script first uses the ``_split`` API (the
    inverse of shrink) to reshape ``bookstore-rag`` into a 2-shard
    ``bookstore-rag-split``, deletes the now-redundant original, and then
    runs the canonical shrink recipe against the split copy.
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
    original_index = "bookstore-rag"
    source_index = "bookstore-rag-split"
    target_index = "bookstore-rag-shrunk"
    # Alias is what clients use; the alias swap is the bit that makes this
    # whole dance invisible to callers.
    alias_name = "bookstore-rag-alias"

    # Step 0 (prerequisite fix): bookstore-rag has only 1 primary shard by
    # default, and _shrink refuses a 1-shard source. Split it into 2 shards
    # first, then drop the now-redundant original.
    client.indices.put_settings(
        index=original_index, body={"index.blocks.write": True}
    )
    step0 = client.indices.split(
        index=original_index,
        target=source_index,
        body={"settings": {"index.number_of_shards": 2, "index.number_of_replicas": 1}},
    )
    print("Step 0: split bookstore-rag into a 2-shard bookstore-rag-split")
    print(json.dumps(step0, indent=2, default=str))
    client.indices.delete(index=original_index)
    print(f"Deleted original {original_index} (data now copied into {source_index})")

    # Step 1: pin every shard onto a real node name (fetch one from _cat/nodes,
    # e.g. the value saved in Lesson 5-1 Step 1) and block writes. Both are
    # preconditions for ``_shrink`` — all primaries must be on one node and
    # the source index must not accept new docs during the operation.
    nodes = client.cat.nodes(params={"h": "name"}, format="json")
    node_name = nodes[0]["name"]
    step1 = client.indices.put_settings(
        index=source_index,
        body={
            "settings": {
                # Require allocation only on the named node.
                "index.routing.allocation.require._name": node_name,
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

    # Step 4b: create the alias on the source first (it must exist before we
    # can "remove" it in the atomic swap below).
    client.indices.put_alias(index=source_index, name=alias_name)
    print(f"\nCreated alias {alias_name} on {source_index}")

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
