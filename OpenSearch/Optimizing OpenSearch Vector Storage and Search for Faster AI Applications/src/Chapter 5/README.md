# Chapter 5 — Production optimizations for OpenSearch clusters

**Chapter 5** · [Vector Storage & Search for AI](../../README.md)

← [Chapter 4](../Chapter%204/README.md) · [How to run labs](../../HANDS-ON-GUIDE.md)

One comprehensive workshop covering shard management, index lifecycle, vector storage modes, security and resilience, and query optimization — all on a **3-node Instaclustr trial cluster** with the AI Search plugin.

## How to use this workshop

- Work top to bottom in **OpenSearch Dashboards → Dev Tools** (Learn mode), or use **[Bruno `Chapter 5`](../../bruno/Chapter%205/)** (Fast mode). Every step has a matching `.bru` numbered in the same order.
- Each step has **Why** (the concept), **Request** (copy into Dev Tools), **Expected**, and **Save** where a value is reused.
- This is a **shared, managed lab cluster.** Steps that change cluster-wide behavior (watermarks, routing awareness, search backpressure) **read the current value first**, apply changes as **`transient`** settings (cleared on a full cluster restart, never persisted), and include an explicit **restore** step. Do not skip the restore steps.
- Some items in the script are **node configuration** (`opensearch.yml`) that you cannot change on a managed cluster. Those are marked **Reference** — read them, but there is nothing to run.

### Reconciling the script with OpenSearch 3.x

| Script shows | Correct on OpenSearch 3.5+ | Where |
|---|---|---|
| `knn_vector` with `data_type: "float16"` for fp16 savings | fp16 is a **Faiss scalar-quantization encoder**: `method.parameters.encoder = { "name": "sq" }` (no `bits` parameter — verified live, `bits` 400s; the only valid `sq` sub-parameter is the optional boolean `clip`). Valid `data_type` values are `float` (default), `byte`, `binary` — there is no `float16`. | Lesson 5-3 |
| `PUT /_security/role/...` (course summary) | OpenSearch Security plugin API is `PUT _plugins/_security/api/roles/<role>` and `_plugins/_security/api/internalusers/<user>`. | Lesson 5-4 |
| `dense_vector` / `dims` (course summary) | Those are Elasticsearch names. OpenSearch uses `knn_vector` / `dimension`. | throughout |
| `nmslib` engine | Removed in OpenSearch 3.x. Use `faiss` (default) or `lucene`. | Lesson 5-2/5-3 |
| Backpressure applied as `persistent` | We use **`transient`** so nothing is left on the shared cluster; a restore step clears it. | Lesson 5-5 |
| Awareness attribute `"zone"` (script/course summary) | This Instaclustr cluster does not set `node.attr.zone`. Every node advertises `node.attr.rack_id` (values `us-west-2a`/`us-west-2b`/`us-west-2c`). Use `cluster.routing.allocation.awareness.attributes: "rack_id"` and `force.rack_id.values` for a realistic, effective example. Verified live: `zone` is silently accepted but never constrains allocation; `rack_id` does. | Lesson 5-1 Step 3 |
| Priority routing attribute `node_type` (power/standard) | Instaclustr nodes only expose `node.attr.rack_id` — there is no `node_type` attribute on this cluster, so Steps 45–46 are confirmed **no-ops** here too (the API call and acknowledgement are still correct and safe to run). | Lesson 5-5 |

## Prerequisites

- [Chapter 1 · Lesson 1](../Chapter%201/README.md) — cluster connectivity and sample data.
- [Chapter 4 · Lesson 4-2](../Chapter%204/README.md#lesson-4-2--optimizing-indexes-for-rag) — the **`bookstore-rag`** index (used by the force-merge and shrink steps). If you do not have it, any populated multi-shard index works; substitute its name.
- 3-node Instaclustr trial with the AI Search plugin. **Lab cluster only — never run these on production.**

## Values to save as you go

| Save | First set in | Reused by |
|---|---|---|
| A **node name** from `_cat/nodes` | 5-1 Step 1 | 5-2 shrink pin |
| Index **`my-index`** | 5-1 Step 5 | 5-1/5-2 |
| Alias **`bookstore-rag-alias`** | 5-2 shrink | client queries after shrink |

---

## Lesson 5-1 — Shards: optimizing, merging, and shard balancing

A **shard** is a self-contained Lucene index. **Primaries** hold your data; **replicas** are redundant copies that add resilience and search throughput. OpenSearch queries all shards in parallel, so shard **size and count** is a balancing act: too many small shards drown you in coordinator overhead; too few large shards hurt recovery and flexibility. Aim for **10–50 GB per shard** (many teams target 20–30 GB).

**Shard-count math (Reference — no API call):**

- **Traditional / text search:** `primary_shards = (current_data × growth_factor) / target_shard_size`. Bookstore: `(800 GB × 1.25) / 40 GB ≈ 25 primary shards`.
- **Vector / k-NN (HNSW):** `vectors_per_shard = (RAM × 50%) / (dimensions × 4 bytes × 1.5 overhead)`. Bookstore: `(64 GB × 0.5) / (768 × 4 × 1.5) ≈ 7M vectors/shard` — so 500k books fit in **one** primary (plan ≥ 1 replica for HA).
- **Hybrid:** compute both, take the larger shard count.

### Step 1: List nodes (and note a node name)

**Why**  
Everything downstream — balancing, routing pins, allocation — is expressed in terms of nodes. `_cat/nodes` shows each node's roles, heap pressure, and disk usage at a glance. On Instaclustr the node names are not `node-1`; grab a real one now.

**Request**

```http
GET _cat/nodes?v&h=name,node.role,master,heap.percent,disk.used_percent
```

**Expected** one row per node (3 on the trial cluster), a `*` under `master` for the elected cluster manager, and heap/disk percentages.

**Save** one **node name** — you need it for the shrink pin in Lesson 5-2.

### Step 2: Read current cluster settings (before changing anything)

**Why**  
On a shared cluster, always capture the current state before you mutate cluster-wide settings, so you can confirm what you changed and restore it. `include_defaults=true` also shows the effective defaults (watermarks, awareness) even when nothing is explicitly set.

**Request**

```http
GET _cluster/settings?include_defaults=true&flat_settings=true
```

**Expected** `persistent`, `transient`, and `defaults` blocks with dotted keys such as `cluster.routing.allocation.disk.watermark.low`.

### Step 3: Configure shard-allocation awareness

**Why**  
Awareness spreads a primary and its replica across **different zones** so one AZ failure never takes out both copies. `force.<attribute>.values` blocks allocation until every listed zone has a node, preventing all replicas from piling into one surviving zone. **This only has a real effect if each node advertises a matching `node.attr`.** Instaclustr nodes do **not** set `node.attr.zone` — check `GET _nodes?filter_path=nodes.*.attributes` first. On this cluster every node advertises **`node.attr.rack_id`** with values `us-west-2a` / `us-west-2b` / `us-west-2c` (one AWS AZ per rack), so the runnable, realistic example uses that attribute instead of the fictitious `zone`.

> **Verified on the real cluster.** `GET _nodes?filter_path=nodes.*.attributes` returned `"rack_id": "us-west-2a"` (etc.) on all 7 nodes — no `zone` attribute exists anywhere, so the original `"attributes": "zone"` call is silently accepted (`acknowledged: true`) but never actually constrains allocation. The corrected call below was applied and confirmed the cluster stayed `green` with `active_shards_percent_as_number: 100.0`.

**Request**

```http
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.awareness.attributes": "rack_id",
    "cluster.routing.allocation.awareness.force.rack_id.values": "us-west-2a,us-west-2b,us-west-2c"
  }
}
```

**Expected** `"acknowledged": true`. (We restore this in Step 14.)

### Step 4: Inspect shard distribution

**Why**  
After any change to awareness, replicas, or routing, confirm shards actually moved. Sorting by node exposes imbalance or shards stuck in `UNASSIGNED` / `INITIALIZING`.

**Request**

```http
GET _cat/shards?v&s=node
```

**Expected** roughly even shard counts per node, `STARTED` on allocated shards, and each primary/replica pair on different nodes.

### Step 5: Force-merge a read-only index

**Why**  
Each write batch creates immutable Lucene **segments**; search visits every segment, so segment sprawl raises latency. **Force merge** compacts them. Use it **only** on read-only / off-peak indexes — any later update or delete leaves tombstones inside a merged segment that waste space and slow search, undoing the gain. Merging to `1` can create huge (>5 GB) segments the background policy then ignores; `5` is a practical balance.

**Prerequisite:** `bookstore-rag` (Chapter 4 · Lesson 4-2).

**Request**

```http
POST bookstore-rag/_forcemerge?max_num_segments=5
```

**Expected** a `_shards` block with successful counts. Can take minutes on a loaded index.

### Step 6: Create a deliberately over-sharded index

**Why**  
This demonstrates the failure mode. A node cannot hold both a primary and its own replica, so once you ask for more shard *copies* than there are data nodes to hold distinct copies, some replicas stay unassigned and the cluster turns **yellow**. Delete first so the step is repeatable.

> **Fixed for a 3-data-node cluster.** With `number_of_replicas: 1` (2 copies per shard) a 3-data-node cluster can place every copy without collision — verified live: the cluster stayed **green**, 100% active shards, nothing unassigned. The failure mode only appears once a shard needs **more copies than there are data nodes**. This cluster has 3 data nodes, so `number_of_replicas: 3` (4 copies per shard: 1 primary + 3 replicas) reliably forces at least one unassigned replica per shard. Verified live: `"status": "yellow"`, `"unassigned_shards": 6` (one per primary shard), `allocation/explain` shows the `same_shard` decider.

**Request**

```http
DELETE my-index
```

A `404` is fine if it did not exist.

```http
PUT my-index
{
  "settings": {
    "number_of_shards": 6,
    "number_of_replicas": 3
  }
}
```

**Expected** `"acknowledged": true`. **Save** the index name **`my-index`**.

### Step 7: Cluster health (before the fix)

**Why**  
`_cluster/health` is your first call in any incident. **Yellow** = replicas unassigned (data intact, redundancy lost). **Red** = a primary is missing (data unsearchable).

**Request**

```http
GET _cluster/health
```

**Expected** `"status": "yellow"` with `"unassigned_shards" > 0`.

### Step 8: Reduce replicas to fix allocation

**Why**  
With too few nodes to place replicas, the lab fix is to lower `number_of_replicas` (production keeps ≥ 1 for HA — the real fix there is adding nodes). Replica count is a **live** setting; no reindex needed.

**Request**

```http
PUT my-index/_settings
{
  "number_of_replicas": 0
}
```

**Expected** `"acknowledged": true`.

### Step 9: Cluster health (after the fix)

**Why**  
Confirm the change worked before moving on.

**Request**

```http
GET _cluster/health
```

**Expected** `"status": "green"`, `"unassigned_shards": 0`.

### Step 10: List shards with the unassigned reason

**Why**  
When shards will not allocate, the `unassigned.reason` column (`NODE_LEFT`, `REPLICA_ADDED`, `CLUSTER_RECOVERED`, `INDEX_CREATED`, …) is the fastest triage signal.

**Request**

```http
GET _cat/shards?v&h=index,shard,prirep,state,node,unassigned.reason
```

**Expected** rows for `my-index`, now `STARTED` with a node name (empty reason).

### Step 11: Per-node disk usage

**Why**  
Unassigned shards in production are often a **disk** problem. `_cat/allocation` shows how full each node is — the input to the watermark logic below.

**Request**

```http
GET _cat/allocation?v&h=node,disk.used_percent,disk.avail
```

**Expected** disk used percent and available space per node.

### Step 12: Explain why a shard is (un)allocated

**Why**  
`allocation/explain` returns plain-language decisions per node — the single best tool for "why won't this shard allocate?" (out of disk, awareness violation, filtered out, etc.).

**Request**

```http
GET _cluster/allocation/explain
{
  "index": "my-index",
  "shard": 1,
  "primary": true
}
```

**Expected** `can_allocate`, `allocate_explanation`, and per-node `deciders` (e.g. `disk_threshold`).

### Step 13: Adjust disk watermarks (transient)

**Why**  
Watermarks protect nodes from filling up: **low (85%)** stop allocating new shards here; **high (90%)** actively relocate shards away; **flood_stage (95%)** make indexes on the node **read-only**. The defaults are good — here you learn the knobs. We use **`transient`** so nothing persists on the shared cluster.

**Request**

```http
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.disk.watermark.low": "85%",
    "cluster.routing.allocation.disk.watermark.high": "90%",
    "cluster.routing.allocation.disk.watermark.flood_stage": "95%"
  }
}
```

**Expected** `"acknowledged": true`.

### Step 14: Restore cluster settings (required)

**Why**  
Return the shared cluster to defaults. `null` clears an override so the built-in default applies again. This clears both the transient watermarks (Step 13) and the persistent awareness (Step 3).

**Request**

```http
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.disk.watermark.low": null,
    "cluster.routing.allocation.disk.watermark.high": null,
    "cluster.routing.allocation.disk.watermark.flood_stage": null
  },
  "persistent": {
    "cluster.routing.allocation.awareness.attributes": null,
    "cluster.routing.allocation.awareness.force.rack_id.values": null
  }
}
```

**Expected** `"acknowledged": true`.

---

## Lesson 5-2 — Index optimization for performance and storage efficiency

Indexes contain shards; segments live inside shards. Good index design plans for the data's **entire lifecycle**: shard sizing, mapping choices, and lifecycle automation. Three levers: **only index what you search**, **separate data by access pattern**, and **automate aging** with Index State Management (ISM).

### Step 15: Create `my-index` with an optimized mapping

**Why**  
Mappings are largely immutable, so decide up front. **`index: false`** stores a field for retrieval but not search (saves space and indexing cost) — good for `internal_notes`. **`enabled: false`** stores an object as-is without indexing any of its sub-fields — good for opaque `inventory_metadata`. This recreates a clean single-shard index for the mapping, reindex, and lifecycle demos.

**Request**

```http
DELETE my-index
```

A `404` is fine.

```http
PUT my-index
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  },
  "mappings": {
    "properties": {
      "book_id": { "type": "keyword" },
      "title": {
        "type": "text",
        "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } }
      },
      "author": { "type": "keyword" },
      "isbn": { "type": "keyword" },
      "genre": { "type": "keyword" },
      "description": { "type": "text" },
      "price": { "type": "float" },
      "in_stock": { "type": "boolean" },
      "published_year": { "type": "integer" },
      "internal_notes": { "type": "text", "index": false },
      "inventory_metadata": { "type": "object", "enabled": false }
    }
  }
}
```

**Expected** `"acknowledged": true`.

### Step 16: Read the mapping

**Why**  
`GET /<index>/_mapping` is your first call when debugging analysis or field types, and the inner `mappings` block is exactly what you'd pass to create the index elsewhere. Confirm `internal_notes` shows `"index": false` and `inventory_metadata` shows `"enabled": false`.

**Request**

```http
GET my-index/_mapping
```

**Expected** JSON keyed by index name with all `properties`.

### Step 17: Tune the refresh interval (live setting)

**Why**  
`refresh_interval` controls how often new writes become searchable. The default is `1s`. Raising it (e.g. `30s`) during a heavy bulk load reduces segment churn and boosts indexing throughput — a setting you **can** change on a live index without a reindex.

**Request**

```http
PUT my-index/_settings
{
  "index": { "refresh_interval": "30s" }
}
```

**Expected** `"acknowledged": true`. (Set back to `null` for default behavior when done.)

### Step 18: Bulk sample documents into `my-index`

**Why**  
The reindex demo (Step 19) is easier to verify with real documents.

**Request**

```http
POST _bulk
{ "index": { "_index": "my-index", "_id": "978-0143127740" } }
{ "book_id": "978-0143127740", "isbn": "978-0143127740", "title": "The Martian", "author": "Andy Weir", "genre": "Science Fiction", "description": "An astronaut stranded on Mars fights to survive.", "price": 16.99, "in_stock": true, "published_year": 2014 }
{ "index": { "_index": "my-index", "_id": "978-0307277677" } }
{ "book_id": "978-0307277677", "isbn": "978-0307277677", "title": "The Road", "author": "Cormac McCarthy", "genre": "Fiction", "description": "A father and son journey through a post-apocalyptic landscape.", "price": 15.95, "in_stock": true, "published_year": 2006 }
```

**Expected** `"errors": false`. Then refresh:

```http
POST my-index/_refresh
```

### Step 19: Reindex with a Painless transform

**Why**  
Some changes cannot be made in place — changing a field **type**, changing shard **count**, or upgrading embedding **dimensions**. `_reindex` copies documents server-side into a freshly designed destination, optionally transforming each doc. Create the destination **first** with the settings you want (never let it auto-create with defaults). `slices` parallelizes the copy; run off-peak.

Create the destination:

```http
PUT my-index-new
{
  "settings": { "index": { "number_of_shards": 1, "number_of_replicas": 0 } },
  "mappings": {
    "properties": {
      "book_id": { "type": "keyword" },
      "title": { "type": "text" },
      "isbn": { "type": "keyword" },
      "genre": { "type": "keyword" },
      "description": { "type": "text" },
      "price": { "type": "float" },
      "in_stock": { "type": "boolean" },
      "published_year": { "type": "integer" }
    }
  }
}
```

Run the reindex:

```http
POST _reindex?slices=5&wait_for_completion=true
{
  "source": { "index": "my-index" },
  "dest": { "index": "my-index-new" },
  "script": {
    "lang": "painless",
    "source": "ctx._source.title = ctx._source.title + ' ' + ctx._source.author; ctx._source.remove('author');"
  }
}
```

**Expected** `"total"`, `"created"`, and `"failures": []`. Verify with `GET my-index-new/_search` — `title` now includes the author and there is no `author` field.

### Step 20–28: Shrink an over-sharded read-only index (the canonical recipe)

**Why**  
**Shrink** rebuilds an index with **fewer primary shards** (target must divide the source count). Use it after time-series roll-off or a bulk load left you over-sharded. The recipe: (1) pin every shard to one node and block writes, (2) `_shrink`, (3) remove the pin so it rebalances, (4) force-merge, (5) atomic alias swap, (6) delete the source.

> **Workshop bug found on the real cluster — `bookstore-rag` has only 1 primary shard.** Chapter 4 · Lesson 4-2 creates `bookstore-rag` without an explicit `number_of_shards`, which defaults to **1**. `_shrink` requires the source to have **more than one** primary shard — verified live: `POST bookstore-rag/_shrink/bookstore-rag-shrunk` returns `400 illegal_argument_exception: can't shrink an index with only one shard`. The fix below first uses the **`_split`** API (the inverse of shrink) to reshape `bookstore-rag` into a 2-shard `bookstore-rag-split`, then runs the canonical shrink recipe against that. This keeps the demo fully runnable against the exact prerequisite index the course builds, and additionally demonstrates `_split`.

**Step 20 — Block writes on `bookstore-rag`** (required before `_split`).

```http
PUT bookstore-rag/_settings
{ "index.blocks.write": true }
```

**Step 21 — Split into `bookstore-rag-split`** (2 primary shards).

```http
POST bookstore-rag/_split/bookstore-rag-split
{
  "settings": { "index.number_of_shards": 2, "index.number_of_replicas": 1 }
}
```

**Expected** `"acknowledged": true`, `"shards_acknowledged": true`. Wait for `GET _cluster/health/bookstore-rag-split?wait_for_status=green&timeout=30s`.

**Step 22 — Delete the original `bookstore-rag`** (its 256 docs are now fully copied into `bookstore-rag-split`).

```http
DELETE bookstore-rag
```

**Step 23 — Pin shards to one node and block writes.** Replace `YOUR_NODE_NAME` with the name saved in Step 1.

```http
PUT bookstore-rag-split/_settings
{
  "settings": {
    "index.routing.allocation.require._name": "YOUR_NODE_NAME",
    "index.blocks.write": true
  }
}
```

Wait until `GET _cat/shards/bookstore-rag-split?v` shows every primary on that node.

**Step 24 — Shrink to the target index.**

```http
POST bookstore-rag-split/_shrink/bookstore-rag-shrunk
{
  "settings": {
    "index.number_of_shards": 1,
    "index.number_of_replicas": 1,
    "index.codec": "best_compression"
  }
}
```

**Step 25 — Remove the routing pin so the shrunk index rebalances.**

```http
PUT bookstore-rag-shrunk/_settings
{
  "index.routing.allocation.require._name": null
}
```

**Step 26 — Force-merge the (now read-only-style) shrunk index to one segment.**

```http
POST bookstore-rag-shrunk/_forcemerge?max_num_segments=1
```

**Step 27 — Atomic alias swap** (clients keep querying `bookstore-rag-alias`; create it on the split index first, then swap).

```http
POST _aliases
{
  "actions": [
    { "add": { "index": "bookstore-rag-split", "alias": "bookstore-rag-alias" } }
  ]
}
```

Then swap:

```http
POST _aliases
{
  "actions": [
    { "remove": { "index": "bookstore-rag-split", "alias": "bookstore-rag-alias" } },
    { "add": { "index": "bookstore-rag-shrunk", "alias": "bookstore-rag-alias" } }
  ]
}
```

**Step 28 — Delete the source index** after verifying the shrunk index serves the alias.

```http
DELETE bookstore-rag-split
```

**Expected across the recipe** each call returns `"acknowledged": true`; `GET _cat/shards/bookstore-rag-shrunk?v` shows fewer shards than `bookstore-rag-split`; `GET bookstore-rag-alias/_count` returns the original 256 docs.

**Fast mode** — `25-block-writes-for-split.bru` → `26-split-bookstore-rag.bru` → `27-delete-original-bookstore-rag.bru` → `28-shrink-pin-block.bru` → `29-shrink-to-target.bru` → `30-shrink-clear-routing.bru` → `31-shrink-force-merge.bru` → `32-shrink-create-alias.bru` → `33-shrink-alias-swap.bru` → `34-shrink-delete-source.bru`

### Step 29: Time-based index with a write alias

**Why**  
For logs/metrics/search-history, create **time-based indexes** (`searches-000001`, …) behind a **write alias** (`is_write_index: true`). Deleting or moving old data is then a whole-index operation — no expensive delete-by-query. Your app writes to the alias and never knows the physical index.

**Request**

```http
PUT searches-000001
{
  "aliases": { "searches-current": { "is_write_index": true } }
}
```

**Expected** `"acknowledged": true`.

### Step 30: Roll the alias over to a new index

**Why**  
`_rollover` creates the next backing index and moves the write alias when the current one hits a size/age/doc threshold — keeping every index in the optimal size range automatically.

**Request**

```http
POST searches-current/_rollover
{
  "conditions": {
    "max_age": "30d",
    "max_size": "50gb",
    "max_docs": 100000
  }
}
```

**Expected** a response with `old_index`, `new_index`, `rolled_over` (likely `false` on a brand-new empty index — the conditions are not met yet), and per-condition results.

### Step 31: Automate aging with an ISM policy

**Why**  
**Index State Management** runs the lifecycle for you: roll over the hot index, then delete after N days. Attach it to an index pattern via `ism_template` so new `searches-*` indexes inherit it. This replaces manual, forgettable maintenance.

**Request**

```http
PUT _plugins/_ism/policies/bookstore-searches-policy
{
  "policy": {
    "description": "Roll over daily/50gb, delete after 90 days",
    "default_state": "hot",
    "states": [
      {
        "name": "hot",
        "actions": [ { "rollover": { "min_size": "50gb", "min_index_age": "30d" } } ],
        "transitions": [ { "state_name": "delete", "conditions": { "min_index_age": "90d" } } ]
      },
      {
        "name": "delete",
        "actions": [ { "delete": {} } ],
        "transitions": []
      }
    ],
    "ism_template": [ { "index_patterns": [ "searches-*" ], "priority": 100 } ]
  }
}
```

**Expected** a `_id` of `bookstore-searches-policy` and the policy body echoed back.

### Step 32: Create `book-embeddings-v2` (versioned k-NN index)

**Why**  
Embedding models change dimensions and similarity behavior. **Versioned index names** let you backfill a new index and swap an alias with no downtime. Store `model_version` per document to audit recall regressions. `faiss` is the production engine; `nmslib` was removed in 3.x.

**Request**

```http
PUT book-embeddings-v2
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "book_id": { "type": "keyword" },
      "title": { "type": "text" },
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "faiss",
          "parameters": { "ef_construction": 128, "m": 16 }
        }
      },
      "model_version": { "type": "keyword" },
      "created_at": { "type": "date" }
    }
  }
}
```

**Expected** `"acknowledged": true`.

### Step 33: Create `book-embeddings-v3` (higher-recall settings)

**Why**  
When v2 recall is too low, move to a **1024-dim** model and a **denser HNSW graph** (`ef_construction: 256`, `m: 32`) — slower indexing, more memory, better recall. Keeping it in a separate index means you migrate gradually without touching the live catalog.

**Request**

```http
PUT book-embeddings-v3
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "book_id": { "type": "keyword" },
      "title": { "type": "text" },
      "embedding": {
        "type": "knn_vector",
        "dimension": 1024,
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "faiss",
          "parameters": { "ef_construction": 256, "m": 32 }
        }
      },
      "model_version": { "type": "keyword" },
      "model_name": { "type": "keyword" },
      "created_at": { "type": "date" }
    }
  }
}
```

**Expected** `"acknowledged": true`.

---

## Lesson 5-3 — Optimizing for vector storage and search

Vectors are memory hogs by design. A 768-dim `float` vector is `768 × 4 = 3072` bytes; the HNSW graph that makes search fast must live in RAM. Bookstore math: `500k × 768 × 4 ≈ 1.5 GB` raw, `≈ 2.25 GB` with ~50% HNSW overhead — fine in one shard. At 10M books that's ~45 GB and must be spread across shards/nodes. Two escape hatches when memory is the constraint: **`on_disk` mode** and **scalar quantization (fp16)**.

### Step 34: Create an `on_disk` archive index

**Why**  
**`on_disk` mode** keeps compressed vectors on disk and rescoring metadata in memory, trading a little latency for a large memory saving — ideal for cold archives searched rarely. Defaults: `faiss` engine, `hnsw` method, `compression_level: 32x`, rescoring on. `on_disk` supports **only** `float` vectors.

**Request**

```http
DELETE book-embeddings-archive
```

A `404` is fine.

```http
PUT book-embeddings-archive
{
  "settings": { "index.knn": true },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "space_type": "l2",
        "data_type": "float",
        "mode": "on_disk"
      }
    }
  }
}
```

**Expected** `"acknowledged": true`.

### Step 35: Trade memory for recall with `compression_level`

**Why**  
`on_disk` defaults to `32x` compression. Lowering it to **`16x`** keeps more precision in memory — higher recall at the cost of a larger footprint. Valid levels: `1x, 2x, 4x, 8x, 16x, 32x` (`4x` uses the `lucene` engine; the rest use `faiss`). Compression > `1x` is `float`-only.

**Request**

```http
PUT book-embeddings-archive-16x
{
  "settings": { "index.knn": true },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "space_type": "l2",
        "data_type": "float",
        "mode": "on_disk",
        "compression_level": "16x"
      }
    }
  }
}
```

**Expected** `"acknowledged": true`.

### Step 36: Create an `in_memory` index (lowest latency)

**Why**  
**`in_memory` mode** keeps full-precision vectors in native memory — lowest query latency, highest cost. This is the default. `data_type: float` is the default 32-bit precision.

**Request**

```http
DELETE book-embeddings-efficient
```

```http
PUT book-embeddings-efficient
{
  "settings": { "index.knn": true },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "space_type": "l2",
        "data_type": "float",
        "mode": "in_memory"
      }
    }
  }
}
```

**Expected** `"acknowledged": true`.

### Step 37: Cut memory in half with fp16 scalar quantization

**Why (and a script correction)**  
The script's `data_type: "float16"` does not exist in OpenSearch. fp16 (**SQfp16**) is a **Faiss scalar-quantization encoder**: set `method.parameters.encoder = { "name": "sq" }`. It stores each dimension as a 16-bit float — **~2× memory reduction** (our bookstore shard drops from ~2.25 GB to ~1.1 GB) with typically < 1% recall loss. Values must be within `[-65504, 65504]`.

> **Second script correction, found on the real cluster.** The `sq` encoder does **not** accept a `bits` parameter — `"encoder": { "name": "sq", "parameters": { "bits": 16 } }` fails live with `mapper_parsing_exception: parameter validation failed for MethodComponentContext parameter [encoder]`. OpenSearch 3.5's Faiss `sq` encoder only implements one quantization type (fp16) and its only valid sub-parameter is the optional boolean `clip` (whether to clip out-of-range values instead of erroring). Verified live: `{ "name": "sq" }` alone, and `{ "name": "sq", "parameters": { "clip": false } }`, both succeed; adding `bits` always 400s.

**Request**

```http
PUT book-embeddings-fp16
{
  "settings": { "index.knn": true },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "space_type": "l2",
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "parameters": {
            "encoder": { "name": "sq" },
            "ef_construction": 128,
            "m": 16
          }
        }
      }
    }
  }
}
```

**Expected** `"acknowledged": true`.

### Step 38: Inspect index stats (memory footprint)

**Why**  
The script's homework: run the stats API to see an index's current load. `_stats` reports doc counts, store size, and (for k-NN) segment info. Compare the fp16 index against a full-precision one to see the savings on real data.

**Request**

```http
GET book-embeddings-fp16/_stats
```

**Expected** `_all.primaries` / `total` blocks with `docs`, `store.size_in_bytes`, etc. Also try the k-NN plugin stats for graph memory:

```http
GET _plugins/_knn/stats?pretty
```

**Expected** per-node k-NN counters (`graph_memory_usage`, `cache_capacity_reached`, hit/miss counts).

---

## Lesson 5-4 — Creating secure, resilient OpenSearch AI applications

Resilience keeps search online when infrastructure fails; security protects customer data. Much of this lesson is **cluster/node configuration** you cannot change on a managed cluster (marked **Reference**), but the **Security plugin API** and **health monitoring** are fully hands-on.

**Reference — resilience (node config, not runnable here):**
- Spread nodes across **multiple AZs**; use shard-allocation awareness (Lesson 5-1 Step 3) so a zone loss never removes both a primary and its replica.
- On-prem: **rack awareness**, redundant power/network, a DR site, and **cross-cluster replication** to it.
- Avoid **split brain** with `cluster.initial_cluster_manager_nodes` and **3 dedicated manager-eligible nodes** (see `opensearch.yml.example` in this chapter folder). Keep JVM heap ≤ 50% of RAM and ≤ 32 GB.

### Step 39: Check cluster health

**Why**  
A healthy cluster is **green** (all primaries + replicas allocated), with balanced shards, stable node count, and heap pressure below ~75%. `level=indices` breaks health down per index so you can spot exactly which catalog category is degraded.

**Request**

```http
GET _cluster/health?level=indices
```

**Expected** top-level `status`, `number_of_nodes`, `active_shards_percent_as_number`, and a per-index breakdown.

### Step 40: Check nodes and JVM heap pressure

**Why**  
Node disconnects and heap pressure are the top warning signs of an unhealthy cluster. `_cat/nodes` confirms all expected nodes are online with their roles; `heap.percent` sustained above ~75% means aggressive garbage collection is coming.

**Request**

```http
GET _cat/nodes?v&h=name,node.role,heap.percent,ram.percent,cpu,load_1m,disk.used_percent
```

**Expected** one row per node with heap/CPU/disk columns. For deeper detail: `GET _nodes/stats/jvm` (heap used, GC counts, circuit breakers).

### Step 41: Create a least-privilege read-only role

**Why**  
**RBAC** with least privilege is the core of the Security plugin. This role can only **read** the bookstore indexes — the pattern for an `Analytics` or `Customer Service` role that must never write. Uses the OpenSearch Security API (`_plugins/_security/api/...`), not the Elasticsearch `_security/role` path shown in the course summary.

**Note (managed clusters):** the Security API requires an admin-privileged user. On Instaclustr, use your admin credentials; if you get `403`, treat Steps 38–40 as **Reference** — the syntax is still correct.

**Request**

```http
PUT _plugins/_security/api/roles/bookstore_read_only
{
  "cluster_permissions": [ "cluster_composite_ops_ro" ],
  "index_permissions": [
    {
      "index_patterns": [ "books*", "bookstore-rag*", "vector-search-index" ],
      "allowed_actions": [ "read", "indices:data/read/search", "indices:data/read/get" ]
    }
  ]
}
```

**Expected** `"status": "CREATED"` (or `"OK"` on update).

**Field-/document-level security (Reference):** add `"fls": [ "~payment_card" ]` to hide a field, or `"dls": "{\"term\":{\"region\":\"US\"}}"` to restrict to matching documents.

### Step 42: Create an internal user bound to the role

**Why**  
Internal users authenticate against OpenSearch's own user database. Binding the user to the role via `opendistro_security_roles` grants exactly the read-only access defined above — no more.

**Request**

```http
PUT _plugins/_security/api/internalusers/bookstore_analyst
{
  "password": "Analyst-Str0ng-Pass!23",
  "opendistro_security_roles": [ "bookstore_read_only" ],
  "backend_roles": [],
  "attributes": { "team": "analytics" }
}
```

**Expected** `"status": "CREATED"`.

### Step 43: Verify the role and user

**Why**  
Confirm the objects exist and the mapping is correct before handing credentials out. Auditing your own security config is a best practice the script calls out directly.

**Request**

```http
GET _plugins/_security/api/roles/bookstore_read_only
```

```http
GET _plugins/_security/api/internalusers/bookstore_analyst
```

**Expected** the role's permissions and the user's roles/attributes (the password is never returned).

**Reference — audit logging & anomaly detection:** enable audit logging in the Security plugin, then point the **Anomaly Detection** plugin at the audit-log index (fields: `user`, `action`, source IP, timestamp; 10-minute interval) as an early-warning layer — not a SIEM replacement. Common mistakes to avoid: default `admin/admin` credentials, port 9200 exposed to the internet, security plugin disabled "for convenience," overly broad roles, no audit logs, unencrypted transport (enable TLS), un-rotated certs.

---

## Lesson 5-5 — Mastering OpenSearch query optimization

Under peak load, all queries competing equally means a checkout can stall behind hundreds of "show me mystery novels." OpenSearch has no per-query priority queue, but you can approximate one with **index/hardware separation**, **request caching**, **recovery priority**, and **search backpressure**. You can also **profile** slow queries and log them.

### Step 44: Create priority-tier demo indexes

**Why**  
Routing rules apply per index, so create lightweight `orders` (high priority) and `book-browse` (low priority) indexes to pin to different node tiers.

**Request**

```http
PUT orders
```

```http
PUT book-browse
```

**Expected** `"acknowledged": true` for each.

### Step 45: Pin `orders` to power-tier nodes

**Why**  
`index.routing.allocation.require.<attr>` forces **all** shards of an index onto nodes whose attribute matches — keeping latency-sensitive `orders` on fast hardware. (`include` = any match, `exclude` = none.) **No-op unless nodes set `node.attr.node_type: power`** — you still see the API and acknowledgement.

**Request**

```http
PUT orders/_settings
{
  "index.routing.allocation.require.node_type": "power"
}
```

**Expected** `"acknowledged": true`.

### Step 46: Pin `book-browse` to standard-tier nodes

**Why**  
Bursty browse traffic lives on cheaper **standard** nodes so it never competes with `orders` for CPU and heap — the "power node" effect achieved by physical index separation (OpenSearch cannot split the search thread pool by query type).

**Request**

```http
PUT book-browse/_settings
{
  "index.routing.allocation.require.node_type": "standard"
}
```

**Expected** `"acknowledged": true`.

### Step 47: Set recovery priority on the critical index

**Why**  
`index.priority` (higher integer = first) controls **recovery order** after a node restart or failure. Critical indexes like `orders` come back online before browse/recommendations, minimizing impact on live operations.

**Request**

```http
PUT orders/_settings
{
  "index.priority": 100
}
```

**Expected** `"acknowledged": true`.

### Step 48: Enable shard request caching

**Why**  
The shard request cache stores results of aggregation/`size:0` queries so hot, repeated requests (current prices, order status) stay fast under load. Enable it per index; higher-value shards effectively stay cached longer than low-priority ones.

**Request**

```http
PUT book-browse/_settings
{
  "index.requests.cache.enable": true
}
```

Then run a cacheable search (`?request_cache=true`, `size:0`):

```http
GET book-browse/_search?request_cache=true
{
  "size": 0,
  "query": { "match_all": {} }
}
```

**Expected** `"acknowledged": true`, then a search response with `hits.total` and no `hits` array entries (size 0). Re-running is served from cache.

### Step 49: Profile a query

**Why**  
`"profile": true` returns a per-shard, per-component timing breakdown — the tool for finding why a query is slow (which clause, rewrite, or collector dominates). Essential before optimizing anything.

**Request**

```http
GET book-browse/_search
{
  "profile": true,
  "query": { "match_all": {} }
}
```

**Expected** a normal search response plus a `profile.shards[]` block with `query`, `rewrite_time`, and `collector` timings in nanoseconds.

### Step 50: Configure slow logs (per index)

**Why**  
Slow logs record queries/fetches exceeding a threshold to the node logs so you can catch pathological requests in production. These are **index-level** settings (safe to set on your demo index) with separate query and fetch thresholds per severity.

**Request**

```http
PUT book-browse/_settings
{
  "index.search.slowlog.threshold.query.warn": "10s",
  "index.search.slowlog.threshold.query.info": "5s",
  "index.search.slowlog.threshold.fetch.warn": "1s"
}
```

**Expected** `"acknowledged": true`.

### Step 51: Read current backpressure settings (before changing)

**Why**  
Capture the baseline before touching cluster-wide backpressure, so you can confirm and restore.

**Request**

```http
GET _cluster/settings?include_defaults=true&flat_settings=true
```

**Expected** a `defaults` block containing `search_backpressure.mode` (default `monitor_only`) and the threshold keys.

### Step 52: Apply backpressure thresholds (transient, monitor_only)

**Why**  
**Search backpressure** cancels expensive in-flight searches when a node is under **duress** (high CPU/heap), trading individual query completion for cluster stability. `monitor_only` **logs what would be cancelled** without cancelling — always tune here before switching to `enforced`. We apply as **`transient`** (the script uses `persistent`; transient is safer on a shared cluster and is cleared in Step 55).

**Request**

```http
PUT _cluster/settings
{
  "transient": {
    "search_backpressure.mode": "monitor_only",
    "search_backpressure.search_shard_task.cpu_time_millis_threshold": 30000,
    "search_backpressure.search_shard_task.elapsed_time_millis_threshold": 45000,
    "search_backpressure.search_task.total_heap_percent_threshold": 0.05,
    "search_backpressure.node_duress.cpu_threshold": 0.90,
    "search_backpressure.node_duress.heap_threshold": 0.70
  }
}
```

**Expected** `"acknowledged": true`.

| Setting | Meaning |
| --- | --- |
| `search_shard_task.cpu_time_millis_threshold: 30000` | a per-shard task using > 30s CPU is "expensive" |
| `search_shard_task.elapsed_time_millis_threshold: 45000` | a per-shard task running > 45s wall-clock is "expensive" |
| `search_task.total_heap_percent_threshold: 0.05` | coordinator buffering > 5% of heap is "expensive" |
| `node_duress.cpu_threshold: 0.90` / `heap_threshold: 0.70` | backpressure only activates when the node itself is stressed |

### Step 53: Apply cancellation rate limits (transient)

**Why**  
Rate limits stop a burst of cancellations from becoming its own outage. `cancellation_rate` caps cancellations per second; `cancellation_burst` allows short spikes.

**Request**

```http
PUT _cluster/settings
{
  "transient": {
    "search_backpressure.search_task.cancellation_rate": 0.05,
    "search_backpressure.search_task.cancellation_burst": 10,
    "search_backpressure.search_shard_task.cancellation_rate": 0.05,
    "search_backpressure.search_shard_task.cancellation_burst": 15
  }
}
```

**Expected** `"acknowledged": true`.

### Step 54: Read backpressure stats

**Why**  
Confirms `monitor_only` is observing traffic and shows per-node counters (what *would* be cancelled) before you ever consider `enforced`.

**Request**

```http
GET _nodes/stats/search_backpressure
```

**Expected** per-node `search_backpressure` blocks: current mode, resource trackers, and cancellation counts.

### Step 55: Restore backpressure settings (required)

**Why**  
Clear the shared cluster back to defaults.

**Request**

```http
PUT _cluster/settings
{
  "transient": {
    "search_backpressure.mode": null,
    "search_backpressure.search_shard_task.cpu_time_millis_threshold": null,
    "search_backpressure.search_shard_task.elapsed_time_millis_threshold": null,
    "search_backpressure.search_task.total_heap_percent_threshold": null,
    "search_backpressure.node_duress.cpu_threshold": null,
    "search_backpressure.node_duress.heap_threshold": null,
    "search_backpressure.search_task.cancellation_rate": null,
    "search_backpressure.search_task.cancellation_burst": null,
    "search_backpressure.search_shard_task.cancellation_rate": null,
    "search_backpressure.search_shard_task.cancellation_burst": null
  }
}
```

**Expected** `"acknowledged": true`.

**Reference — thread pools (node config):** in `opensearch.yml` you can size the built-in `search` and `write` thread pools (`size`, `queue_size`) but you **cannot** create custom-named pools or route query types to pools by name. Priority separation is achieved by index/hardware separation (Steps 42–43). See `opensearch.yml.example` in this chapter folder.

---

## Cleanup

Remove the lab indexes, policy, and security objects, and confirm cluster settings were restored.

```http
DELETE my-index,my-index-new,searches-000001,orders,book-browse,book-embeddings-v2,book-embeddings-v3,book-embeddings-archive,book-embeddings-archive-16x,book-embeddings-efficient,book-embeddings-fp16,bookstore-rag-shrunk
```

> If the shrink recipe (Steps 20–28) is still mid-flight, also verify `bookstore-rag`, `bookstore-rag-split`, and the `bookstore-rag-alias` alias are cleaned up per that recipe's own steps before running this cleanup.

```http
DELETE _plugins/_ism/policies/bookstore-searches-policy
```

```http
DELETE _plugins/_security/api/internalusers/bookstore_analyst
```

```http
DELETE _plugins/_security/api/roles/bookstore_read_only
```

Confirm no lab settings remain (should show no `search_backpressure.*`, awareness, or watermark overrides under `persistent`/`transient`):

```http
GET _cluster/settings?flat_settings=true
```

> Steps 5 and 20–28 modify (and ultimately delete) `bookstore-rag` from Chapter 4. If you plan to re-run Chapter 4 labs, rebuild that index with Chapter 4 · Lesson 4-2.

## What you learned

- **5-1:** shard sizing math, awareness, `_cat/shards` / `_cat/allocation`, force merge, replicas, `allocation/explain`, disk watermarks.
- **5-2:** `index:false` / `enabled:false` mappings, `refresh_interval`, reindex with Painless, the shrink + alias-swap recipe, time-based indexes, rollover, and ISM.
- **5-3:** `on_disk` vs `in_memory`, `compression_level`, and correct **fp16 scalar quantization** via the Faiss `sq` encoder.
- **5-4:** cluster health monitoring plus creating least-privilege **roles and users** through the Security plugin API.
- **5-5:** index/hardware separation, `index.priority`, request caching, `_profile`, slow logs, and search backpressure — applied safely with transient settings and restores.

## Reference scripts (Python)

Optional Python mirrors of selected steps live in this folder. Configure `src/.env` (see the [hands-on guide](../../HANDS-ON-GUIDE.md)) and run e.g. `python 03-l1-force-merge.py`.

| Script | Covers |
| --- | --- |
| `01-l1-routing-awareness.py` | 5-1 Step 3 |
| `02-l1-check-shard-distribution.py` | 5-1 Step 4 |
| `03-l1-force-merge.py` | 5-1 Step 5 |
| `04-l1-index-too-many-shards.py` | 5-1 Step 6 |
| `05-l1-cluster-health-and-replicas.py` | 5-1 Steps 7–12 |
| `06-l1-watermark-settings.py` | 5-1 Step 13 |
| `07-l2-create-my-index-bookstore.py` | 5-2 Step 15 |
| `08-l2-get-mapping.py` | 5-2 Step 16 |
| `09-l2-shrink-index.py` | 5-2 Steps 20–28 (includes the `_split` prerequisite fix) |
| `10-l2-reindex-books.py` | 5-2 Step 19 |
| `11-l2-create-book-embeddings-v2.py` | 5-2 Step 32 |
| `12-l2-create-book-embeddings-v3.py` | 5-2 Step 33 |
| `13-l3-vector-storage-modes.py` | 5-3 Steps 34–37 |
| `14-l5-priority-index-routing.py` | 5-5 Steps 44–46 |
| `15-l5-search-backpressure.py` | 5-5 Steps 52–54 |
