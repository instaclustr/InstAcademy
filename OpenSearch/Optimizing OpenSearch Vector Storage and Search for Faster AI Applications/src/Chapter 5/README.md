# Chapter 5 — Production optimizations for OpenSearch clusters

**Chapter 5** · [Vector Storage & Search for AI](../../README.md)

← [Chapter 4](../Chapter%204/README.md) · [How to run labs](../../HANDS-ON-GUIDE.md)

One comprehensive workshop covering shard management, index lifecycle, vector storage modes, security and resilience, and query optimization — all on a **3-node Instaclustr trial cluster** with the AI Search plugin.

## How to use this workshop

- Work top to bottom in **OpenSearch Dashboards → Dev Tools** (Learn mode), or use **[Bruno `Chapter 5`](../../bruno/Chapter%205/)** (Fast mode). Every step has matching `.bru` requests in run order (the file numbering has gaps where steps were consolidated).
- Each step has **Why** (the concept), **Request** (copy into Dev Tools), **Expected**, and **Save** where a value is reused.
- This is a **shared, managed lab cluster.** Cluster-wide mutations (watermarks, routing awareness, search backpressure, priority routing) are shown as **Reference** — syntax to know, nothing to run. The hands-on steps only touch lab indexes you create and delete yourself.
- Some items in the script are **node configuration** (`opensearch.yml`) that you cannot change on a managed cluster. Those are marked **Reference** — read them, but there is nothing to run.

### Reconciling the script with OpenSearch 3.x

| Script shows | Correct on OpenSearch 3.5+ | Where |
|---|---|---|
| `knn_vector` with `data_type: "float16"` for fp16 savings | fp16 is a **Faiss scalar-quantization encoder**: `method.parameters.encoder = { "name": "sq" }` (no `bits` parameter — verified live, `bits` 400s; the only valid `sq` sub-parameter is the optional boolean `clip`). Valid `data_type` values are `float` (default), `byte`, `binary` — there is no `float16`. | Lesson 5-3 |
| `PUT /_security/role/...` (course summary) | OpenSearch Security plugin API is `PUT _plugins/_security/api/roles/<role>` and `_plugins/_security/api/internalusers/<user>`. | Lesson 5-4 |
| `dense_vector` / `dims` (course summary) | Those are Elasticsearch names. OpenSearch uses `knn_vector` / `dimension`. | throughout |
| `nmslib` engine | Removed in OpenSearch 3.x. Use `faiss` (default) or `lucene`. | Lesson 5-2/5-3 |
| Backpressure applied as `persistent` | Shown as **Reference**; when tuning in production, apply as `transient` first and monitor before enforcing. | Lesson 5-5 (Reference) |
| Awareness attribute `"zone"` (script/course summary) | This Instaclustr cluster does not set `node.attr.zone`. Every node advertises `node.attr.rack_id` (values `us-west-2a`/`us-west-2b`/`us-west-2c`). Use `cluster.routing.allocation.awareness.attributes: "rack_id"` and `force.rack_id.values` for a realistic, effective example. Verified live: `zone` is silently accepted but never constrains allocation; `rack_id` does. | Lesson 5-1 (Reference) |
| Priority routing attribute `node_type` (power/standard) | Instaclustr nodes only expose `node.attr.rack_id` — there is no `node_type` attribute on this cluster, so the priority-routing examples are confirmed **no-ops** here (shown as Reference). | Lesson 5-5 |

## Prerequisites

- [Chapter 1 · Lesson 1](../Chapter%201/README.md) — cluster connectivity and sample data.
- [Chapter 4 · Lesson 4-2](../Chapter%204/README.md#lesson-4-2--optimizing-indexes-for-rag) — the **`bookstore-rag`** index is referenced by the read-along shrink recipe in Lesson 5-2; nothing in this chapter modifies it.
- 3-node Instaclustr trial with the AI Search plugin. **Lab cluster only — never run these on production.**

## Values to save as you go

One value carries through the chapter: the index **`my-index`** (created in 5-1 Step 1, given an optimized mapping in 5-2, and used by every Lesson 5-5 step).

---

## Lesson 5-1 — Shards: optimizing, merging, and shard balancing

A **shard** is a self-contained Lucene index. **Primaries** hold your data; **replicas** are redundant copies that add resilience and search throughput. OpenSearch queries all shards in parallel, so shard **size and count** is a balancing act: too many small shards drown you in coordinator overhead; too few large shards hurt recovery and flexibility. Aim for **10–50 GB per shard** (many teams target 20–30 GB).

**Shard-count math (Reference — no API call):**

- **Traditional / text search:** `primary_shards = (current_data × growth_factor) / target_shard_size`. Bookstore: `(800 GB × 1.25) / 40 GB ≈ 25 primary shards`.
- **Vector / k-NN (HNSW):** `vectors_per_shard = (RAM × 50%) / (dimensions × 4 bytes × 1.5 overhead)`. Bookstore: `(64 GB × 0.5) / (768 × 4 × 1.5) ≈ 7M vectors/shard` — so 500k books fit in **one** primary (plan ≥ 1 replica for HA).
- **Hybrid:** compute both, take the larger shard count.

> **Reference — shard-allocation awareness.** Awareness spreads a primary and its replica across **different zones** so one AZ failure never takes out both copies: set `cluster.routing.allocation.awareness.attributes` to a node attribute, and `force.<attribute>.values` to block allocation until every listed zone has a node. **It only works when each node advertises a matching `node.attr`** — verified live on this cluster: nodes carry `node.attr.rack_id` (`us-west-2a/b/c`, one AWS AZ per rack), so `"attributes": "rack_id"` constrains allocation while the video's fictitious `"zone"` is silently accepted and does nothing. Check your own cluster with `GET _nodes?filter_path=nodes.*.attributes`. It's a persistent, cluster-wide setting on a shared lab cluster, so treat it as syntax to know rather than a step to run; after any allocation change, `GET _cat/shards?v&s=node` confirms shards actually moved.

> **Force merge (already done in Chapter 4).** Chapter 4's fast-bulk recipe (Step 6) already force-merged `bookstore-rag` to `max_num_segments=5`, so there is nothing to re-run here. What's new is the **operations framing**:

> - Each write batch creates immutable Lucene **segments**; search visits every segment, so segment sprawl raises latency, and force merge compacts them.
> - Use it **only** on read-only / off-peak indexes — any later update or delete leaves tombstones inside a merged segment that waste space and slow search, undoing the gain.
> - Merging to `1` can create huge (>5 GB) segments the background merge policy then ignores; `5` is a practical balance for an index that still receives occasional writes.

### Step 1: Create a deliberately over-sharded index and watch the cluster go yellow

The best way to learn cluster triage is to break a cluster you're allowed to break. In this step you deliberately create the most common allocation failure in the wild: asking for more shard *copies* than there are data nodes to hold them. A node will never host both a primary and its own replica (that would defeat the point of a replica), so the extra copies simply have nowhere to go, they sit unassigned, and the cluster turns **yellow**. You'll see the symptom now and fix it in Step 2. Delete first so the step is repeatable.

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

**Expected** `"acknowledged": true`. **Save** the index name **`my-index`**. Then check cluster health — `_cluster/health` is your first call in any incident. **Yellow** = replicas unassigned (data intact, redundancy lost). **Red** = a primary is missing (data unsearchable):

```http
GET _cluster/health
```

**Expected** `"status": "yellow"` with `"unassigned_shards" > 0`.

**Fast mode** — `06-delete-my-index-overshard.bru` → `07-create-oversharded-index.bru` → `08-cluster-health-before.bru`

### Step 2: Reduce replicas to fix allocation, then verify

Now play the on-call engineer and bring the cluster back to green. Since the problem is more replica copies than nodes to hold them, the lab fix is to lower `number_of_replicas`. Note that replica count is a **live** setting: one API call, no reindex, and the cluster heals in seconds. (In production you'd keep at least 1 replica for high availability; the real fix there is adding nodes, not shedding redundancy.)

**Request**

```http
PUT my-index/_settings
{
  "number_of_replicas": 0
}
```

Verify with health and the shard list — the `unassigned.reason` column (`NODE_LEFT`, `REPLICA_ADDED`, `CLUSTER_RECOVERED`, `INDEX_CREATED`, …) is the fastest triage signal when shards won't allocate:

```http
GET _cluster/health
```

```http
GET _cat/shards?v&h=index,shard,prirep,state,node,unassigned.reason
```

**Expected** `"status": "green"`, `"unassigned_shards": 0`, and `my-index` rows now `STARTED` with a node name (empty reason).

**Fast mode** — `09-set-replicas-zero.bru` → `10-cluster-health-after.bru` → `11-cat-shards-unassigned.bru`

### Step 3: Diagnose allocation: per-node disk and allocation explain

You fixed this incident because you caused it and knew the answer. Real incidents don't come with an explanation attached, so meet the two tools that provide one. `_cat/allocation` shows how full each node's disk is, which matters because unassigned shards in production are very often a disk problem in disguise. And `allocation/explain` is the closest thing OpenSearch has to a "why" button: it returns plain-language, per-node decisions for exactly why a shard can or cannot allocate (out of disk, awareness violation, filtered out, and so on). Learn this pair now and your next 3 a.m. yellow cluster becomes a five-minute diagnosis.

**Request**

```http
GET _cat/allocation?v&h=node,disk.used_percent,disk.avail
```

```http
GET _cluster/allocation/explain
{
  "index": "my-index",
  "shard": 1,
  "primary": true
}
```

**Expected** disk used percent per node, then `can_allocate`, `allocate_explanation`, and per-node `deciders` (e.g. `disk_threshold`).

**Fast mode** — `12-cat-allocation-disk.bru` → `13-allocation-explain.bru`

> **Disk watermarks (Reference).** Watermarks protect nodes from filling up: **low (85%)** stop allocating new shards here; **high (90%)** actively relocate shards away; **flood_stage (95%)** make indexes on the node **read-only**. The keys are `cluster.routing.allocation.disk.watermark.{low,high,flood_stage}`, settable transiently. The defaults are good — know the knobs, don't change them on a shared lab cluster.

---

## Lesson 5-2 — Index optimization for performance and storage efficiency

Indexes contain shards; segments live inside shards. Good index design plans for the data's **entire lifecycle**: shard sizing, mapping choices, and lifecycle automation. Three levers: **only index what you search**, **separate data by access pattern**, and **automate aging** with Index State Management (ISM).

### Step 4: Create `my-index` with an optimized mapping, then read it back

Here's an index-design principle that saves real money at scale: **only index what you search**. By default OpenSearch builds search structures for every field, but plenty of fields are only ever *retrieved*, never queried. This mapping shows the two opt-outs. **`index: false`** stores a field's value but builds no search structures for it, perfect for `internal_notes` that staff read but nobody queries. **`enabled: false`** goes further and stores an object completely as-is without indexing any sub-field, perfect for opaque blobs like `inventory_metadata`. Decide these up front, because mappings are largely immutable once documents land. This also recreates a clean single-shard `my-index` for the lifecycle demos ahead.

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

Then read it back — `GET /<index>/_mapping` is your first call when debugging analysis or field types, and the inner `mappings` block is exactly what you'd pass to create the index elsewhere:

```http
GET my-index/_mapping
```

**Expected** `"acknowledged": true` for the create, then JSON keyed by index name with all `properties` — confirm `internal_notes` shows `"index": false` and `inventory_metadata` shows `"enabled": false`.

**Fast mode** — `16-delete-my-index-mapping.bru` → `17-create-my-index-bookstore.bru` → `18-get-mapping.bru`

> **Refresh interval (already covered).** `refresh_interval` is the live, no-reindex setting you tuned in Chapter 2 Step 15 and toggled off/on around Chapter 4's fast bulk load (Step 6). The index-design takeaway: decide it per index, alongside the mapping, based on how fresh search results must be — the default `1s` suits interactive writes; `30s` (or `-1`) suits batch loads. For the two sample documents below, the default is fine.

### Step 5: Bulk sample documents into `my-index`

Two quick documents and one refresh. It's a small step, but the caching, profiling, and slow-log work in Lesson 5-5 all runs against this index, and observability demos are far more convincing when there's real data behind them.

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

**Fast mode** — `20-bulk-my-index.bru` → `21-refresh-my-index.bru`

> **Reindex with a Painless transform (already done in Chapter 1).** Some changes cannot be made in place — changing a field **type**, changing shard **count**, or upgrading embedding **dimensions**. The fix is always the same server-side pattern you ran in Chapter 1 Step 16: create the destination **first** with the settings you want (never let it auto-create with defaults), then `POST _reindex` with a Painless `script` transforming each document in flight. Add `slices=5` to parallelize; run off-peak. Nothing new to run here.

### Reference: Shrink an over-sharded read-only index (the canonical recipe)

**Read-along — nothing to run.** This recipe would reshape and ultimately delete Chapter 4's `bookstore-rag`; on the lab cluster the payoff doesn't justify rebuilding that index, but in production this is *the* zero-downtime resharding pattern. **Shrink** rebuilds an index with **fewer primary shards** (the target count must evenly divide the source count), and you reach for it after time-series roll-off or when a bulk load left you over-sharded. The full sequence: (1) pin every shard to one node and block writes, (2) `_shrink`, (3) remove the pin so it rebalances, (4) force-merge, (5) atomic alias swap, (6) delete the source. Study each move below:

> **Workshop bug found on the real cluster — `bookstore-rag` has only 1 primary shard.** Chapter 4 · Lesson 4-2 creates `bookstore-rag` without an explicit `number_of_shards`, which defaults to **1**. `_shrink` requires the source to have **more than one** primary shard — verified live: `POST bookstore-rag/_shrink/bookstore-rag-shrunk` returns `400 illegal_argument_exception: can't shrink an index with only one shard`. The fix below first uses the **`_split`** API (the inverse of shrink) to reshape `bookstore-rag` into a 2-shard `bookstore-rag-split`, then runs the canonical shrink recipe against that. This keeps the demo fully runnable against the exact prerequisite index the course builds, and additionally demonstrates `_split`.

**1 — Block writes on `bookstore-rag`** (required before `_split`).

```http
PUT bookstore-rag/_settings
{ "index.blocks.write": true }
```

**2 — Split into `bookstore-rag-split`** (2 primary shards).

```http
POST bookstore-rag/_split/bookstore-rag-split
{
  "settings": { "index.number_of_shards": 2, "index.number_of_replicas": 1 }
}
```

**Expected** `"acknowledged": true`, `"shards_acknowledged": true`. Wait for `GET _cluster/health/bookstore-rag-split?wait_for_status=green&timeout=30s`.

**3 — Delete the original `bookstore-rag`** (its 256 docs are now fully copied into `bookstore-rag-split`).

```http
DELETE bookstore-rag
```

**4 — Pin shards to one node and block writes.** Replace `YOUR_NODE_NAME` with a node name from `GET _cat/nodes?v` (in Bruno, set **`nodeName`** in the **Local** environment).

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

**5 — Shrink to the target index.**

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

**6 — Remove the routing pin so the shrunk index rebalances.**

```http
PUT bookstore-rag-shrunk/_settings
{
  "index.routing.allocation.require._name": null
}
```

**7 — Force-merge the (now read-only-style) shrunk index to one segment.**

```http
POST bookstore-rag-shrunk/_forcemerge?max_num_segments=1
```

**8 — Atomic alias swap** (clients keep querying `bookstore-rag-alias`; create it on the split index first, then swap).

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

**9 — Delete the source index** after verifying the shrunk index serves the alias.

```http
DELETE bookstore-rag-split
```

**Expected across the recipe** each call returns `"acknowledged": true`; `GET _cat/shards/bookstore-rag-shrunk?v` shows fewer shards than `bookstore-rag-split`; `GET bookstore-rag-alias/_count` returns the original 256 docs.

### Step 6: Automate the index lifecycle: write alias, rollover, and ISM

Some data never stops arriving: logs, metrics, search history. Let it pile into one index and that index grows without bound until it becomes a problem someone inherits. This step builds the standard escape hatch in three moves that hand off to each other. First, a **time-based index** (`searches-000001`) behind a **write alias** (`is_write_index: true`), so your app writes to the alias and never knows which physical index is current, and aging out old data becomes a cheap whole-index delete instead of an expensive delete-by-query. Second, `_rollover`, which creates the next backing index and moves the write alias whenever the current one hits a size, age, or doc-count threshold. Third, an **ISM policy** that runs the whole cycle automatically, because any maintenance that depends on a human remembering it will eventually be forgotten.

**Request**

```http
PUT searches-000001
{
  "aliases": { "searches-current": { "is_write_index": true } }
}
```

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

**Expected** `"acknowledged": true` for the create, then a rollover response with `old_index`, `new_index`, `rolled_over` (likely `false` on a brand-new empty index — the conditions are not met yet), and per-condition results.

Finally, hand the cycle to **Index State Management**: roll over the hot index, then delete after N days, attached to an index pattern via `ism_template` so new `searches-*` indexes inherit it — replacing manual, forgettable maintenance.

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

**Fast mode** — `35-time-based-index.bru` → `36-rollover-alias.bru` → `37-create-ism-policy.bru`

> **Versioned k-NN indexes (read-along).** Embedding models change dimensions and similarity behavior, and a `knn_vector` mapping can't be edited in place. The production pattern: **versioned index names** (`book-embeddings-v2`, `-v3`, …) behind an alias — backfill the new version, swap the alias, zero downtime. Store `model_version` / `model_name` per document to audit recall regressions. A v2→v3 upgrade is typically the same mapping with a higher `dimension` (e.g. 768 → 1024) and a denser HNSW graph (`ef_construction: 256`, `m: 32`) — slower indexing, more memory, better recall — kept in a separate index so you migrate gradually without touching the live catalog. The naming pattern is the lesson; there's no need to create empty indexes to see it. (`faiss` is the production engine; `nmslib` was removed in 3.x.)

---

## Lesson 5-3 — Optimizing for vector storage and search

Vectors are memory hogs by design. A 768-dim `float` vector is `768 × 4 = 3072` bytes; the HNSW graph that makes search fast must live in RAM. Bookstore math: `500k × 768 × 4 ≈ 1.5 GB` raw, `≈ 2.25 GB` with ~50% HNSW overhead — fine in one shard. At 10M books that's ~45 GB and must be spread across shards/nodes. Two escape hatches when memory is the constraint: **`on_disk` mode** and **scalar quantization (fp16)**.

> **Storage modes recap (already covered in Chapter 1 — nothing to run).** You built an `on_disk` index in Chapter 1 Step 6 (`vector-disk-demo`); the mechanics are identical at production scale, only `dimension: 768` changes. The production framing worth pinning before the fp16 step:
>
> - **`on_disk`** keeps compressed vectors on disk and rescoring metadata in memory — a little latency for a large memory saving, ideal for cold archives searched rarely. Defaults: `faiss` engine, `hnsw` method, **`compression_level: 32x`**, rescoring on; `float` vectors only.
> - **`compression_level`** tunes that trade: `16x` keeps more precision in memory than the default `32x` (higher recall, larger footprint). Valid levels `1x`–`32x`; one detail Chapter 1 didn't cover — **`4x` uses the `lucene` engine**, the rest use `faiss`. Compression > `1x` is `float`-only.
> - **`in_memory`** keeps full-precision vectors in native memory — lowest latency, highest cost. It is the **default**: every `knn_vector` index you've created without a `mode` (Chapter 2's `vector-search-index`, Chapter 4's `bookstore-rag`) is already `in_memory` with `data_type: float` (32-bit).

### Step 7: Cut memory in half with fp16 scalar quantization

If someone offered to cut your vector memory bill in half for under 1% recall loss, you'd take that trade every time, and that's exactly what fp16 quantization is: each dimension stored as a 16-bit float instead of 32, dropping our bookstore shard math from ~2.25 GB to ~1.1 GB. One correction to the video script before you run it: `data_type: "float16"` does not exist in OpenSearch. The real mechanism is a **Faiss scalar-quantization encoder**, set via `method.parameters.encoder = { "name": "sq" }`. Values must fit within `[-65504, 65504]`, which normalized embeddings always do.

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

**Fast mode** — `45-create-fp16-quantized.bru`

### Step 8: Inspect index stats (memory footprint)

A claim like "half the memory" deserves verification, and this is the API you'd verify it with. `_stats` reports doc counts, store size, and (for k-NN indexes) segment info, making it the go-to for answering "what is this index actually costing me right now?" Run it against `book-embeddings-fp16`, and when you want a real before/after, compare against a full-precision index like Chapter 4's populated `bookstore-rag` once data is loaded.

**Request**

```http
GET book-embeddings-fp16/_stats
```

**Expected** `_all.primaries` / `total` blocks with `docs`, `store.size_in_bytes`, etc. Also try the k-NN plugin stats for graph memory:

```http
GET _plugins/_knn/stats?pretty
```

**Expected** per-node k-NN counters (`graph_memory_usage`, `cache_capacity_reached`, hit/miss counts).

**Fast mode** — `46-index-stats.bru` → `47-knn-stats.bru`

---

## Lesson 5-4 — Creating secure, resilient OpenSearch AI applications

Resilience keeps search online when infrastructure fails; security protects customer data. Much of this lesson is **cluster/node configuration** you cannot change on a managed cluster (marked **Reference**), but the **Security plugin API** and **health monitoring** are fully hands-on.

**Reference — resilience (node config, not runnable here):**
- Spread nodes across **multiple AZs**; use shard-allocation awareness (Lesson 5-1 reference) so a zone loss never removes both a primary and its replica.
- On-prem: **rack awareness**, redundant power/network, a DR site, and **cross-cluster replication** to it.
- Avoid **split brain** with `cluster.initial_cluster_manager_nodes` and **3 dedicated manager-eligible nodes** (see `opensearch.yml.example` in this chapter folder). Keep JVM heap ≤ 50% of RAM and ≤ 32 GB.

> **Monitoring quick reference.** You already used `_cluster/health` for triage in Lesson 5-1; the production monitoring loop adds two refinements: `GET _cluster/health?level=indices` breaks health down per index so you can spot exactly which catalog category is degraded, and `GET _cat/nodes?v&h=name,node.role,heap.percent,ram.percent,cpu,load_1m,disk.used_percent` watches the top warning signs — node disconnects and `heap.percent` sustained above ~75% (aggressive garbage collection is coming). For deeper detail: `GET _nodes/stats/jvm` (heap used, GC counts, circuit breakers).

> **Reference — least-privilege security (roles and users).** RBAC with least privilege is the core of the Security plugin, but it's cluster administration rather than vector-search optimization, so treat this as syntax to know rather than steps to run. The OpenSearch Security API (not Elasticsearch's `_security/role` path) creates a read-only role scoped to specific index patterns:
>
> ```
> PUT _plugins/_security/api/roles/bookstore_read_only
> { "cluster_permissions": [ "cluster_composite_ops_ro" ],
>   "index_permissions": [ { "index_patterns": [ "books*", "bookstore-rag*" ],
>       "allowed_actions": [ "read", "indices:data/read/search", "indices:data/read/get" ] } ] }
> ```
>
> then an internal user bound to it via `PUT _plugins/_security/api/internalusers/<user>` with `"opendistro_security_roles": [ "bookstore_read_only" ]`, and `GET` on both endpoints to audit before handing credentials out. Field-level (`"fls": [ "~payment_card" ]`) and document-level (`"dls"`) security restrict what a role can see inside an index. Note the Security API requires admin privileges on a managed cluster.

**Reference — audit logging & anomaly detection:** enable audit logging in the Security plugin, then point the **Anomaly Detection** plugin at the audit-log index (fields: `user`, `action`, source IP, timestamp; 10-minute interval) as an early-warning layer — not a SIEM replacement. Common mistakes to avoid: default `admin/admin` credentials, port 9200 exposed to the internet, security plugin disabled "for convenience," overly broad roles, no audit logs, unencrypted transport (enable TLS), un-rotated certs.

---

## Lesson 5-5 — Mastering OpenSearch query optimization

Under peak load, all queries competing equally means a checkout can stall behind hundreds of "show me mystery novels." OpenSearch has no per-query priority queue, but you can approximate one with **index/hardware separation**, **request caching**, **recovery priority**, and **search backpressure**. You can also **profile** slow queries and log them.

> **Reference — priority tiers and recovery order.** OpenSearch has no per-query priority queue; the approximation is **physical index separation**: pin latency-sensitive indexes (e.g. `orders`) to fast nodes with `index.routing.allocation.require.<attr>: power` and bursty browse traffic to cheaper nodes with `: standard` (`include` = any match, `exclude` = none). This only works when nodes advertise a matching `node.attr` — **this Instaclustr cluster has no `node_type` attribute, so the calls would be silent no-ops here** (verified). Related: `index.priority` (higher integer = first) controls **recovery order** after a node restart, so critical indexes come back online before browse/recommendations.

### Step 9: Enable shard request caching

Think about how much of your search traffic is the *same* few requests fired over and over: current prices, order status, the dashboard someone keeps refreshing. Recomputing those from scratch every time is pure waste. The shard request cache stores the results of aggregation and `size: 0` queries at the shard level, so hot, repeated requests get answered from memory while the cluster's compute goes to queries that are genuinely new. Enable it per index, and note the practical effect: your highest-value, most-hammered shards end up staying cached the longest. We use the populated `my-index` from Lesson 5-2.

**Request**

```http
PUT my-index/_settings
{
  "index.requests.cache.enable": true
}
```

Then run a cacheable search (`?request_cache=true`, `size:0`):

```http
GET my-index/_search?request_cache=true
{
  "size": 0,
  "query": { "match_all": {} }
}
```

**Expected** `"acknowledged": true`, then a search response with `hits.total` and no `hits` array entries (size 0). Re-running is served from cache.

**Fast mode** — `59-enable-request-cache.bru` → `60-cacheable-search.bru`

### Step 10: Profile a query

Never optimize a slow query on a hunch. Adding `"profile": true` to any search returns a per-shard, per-component timing breakdown, showing exactly which clause, rewrite, or collector is eating the time, so you fix the actual bottleneck instead of the suspected one. Make it the first move whenever someone reports "search is slow." (One caveat from Chapter 4: `profile` combined with a `hybrid` query 500s on OpenSearch 3.5.0; plain queries like this one work fine.)

**Request**

```http
GET my-index/_search
{
  "profile": true,
  "query": { "match_all": {} }
}
```

**Expected** a normal search response plus a `profile.shards[]` block with `query`, `rewrite_time`, and `collector` timings in nanoseconds.

**Fast mode** — `61-profile-query.bru`

### Step 11: Configure slow logs (per index)

Profiling works when you already know which query is slow, but in production the pathological query usually strikes while nobody is watching. Slow logs are the tripwire: any query or fetch that exceeds your thresholds gets recorded to the node logs with its full body, so the evidence is waiting for you instead of vanished. These are **index-level** settings (safe to set on your demo index) with separate query and fetch thresholds per severity, letting you decide per index what counts as "worryingly slow."

**Request**

```http
PUT my-index/_settings
{
  "index.search.slowlog.threshold.query.warn": "10s",
  "index.search.slowlog.threshold.query.info": "5s",
  "index.search.slowlog.threshold.fetch.warn": "1s"
}
```

**Expected** `"acknowledged": true`.

**Fast mode** — `62-set-slow-logs.bru`

> **Reference — search backpressure.** **Search backpressure** cancels expensive in-flight searches when a node is under **duress** (high CPU/heap), trading individual query completion for cluster stability. The knobs, all under `search_backpressure.*` cluster settings: `mode` (`monitor_only` **logs what would be cancelled** without cancelling — always tune here before ever switching to `enforced`); per-shard-task thresholds that define "expensive" (`cpu_time_millis_threshold: 30000` = >30s CPU, `elapsed_time_millis_threshold: 45000` = >45s wall-clock, `total_heap_percent_threshold: 0.05` = coordinator buffering >5% of heap); `node_duress.cpu_threshold: 0.90` / `heap_threshold: 0.70` so backpressure only activates when the node itself is stressed; and `cancellation_rate` / `cancellation_burst` caps so a wave of cancellations never becomes its own outage. Observe with `GET _nodes/stats/search_backpressure` (per-node mode, resource trackers, would-be cancellation counts). On an idle lab cluster the counters read zero, so there's nothing to run here — when you tune it in production, apply as `transient` first, watch `monitor_only` stats, and only then consider `enforced`.

**Reference — thread pools (node config):** in `opensearch.yml` you can size the built-in `search` and `write` thread pools (`size`, `queue_size`) but you **cannot** create custom-named pools or route query types to pools by name. Priority separation is achieved by index/hardware separation (see the priority-tiers reference above). See `opensearch.yml.example` in this chapter folder.

---

## Cleanup

Remove the lab indexes and policy.

```http
DELETE my-index,searches-000001,book-embeddings-fp16
```

> Earlier revisions of this workshop also created `my-index-new`, `orders`, `book-browse`, `book-embeddings-v2`, `book-embeddings-v3`, `book-embeddings-archive`, `book-embeddings-archive-16x`, `book-embeddings-efficient`, `bookstore-rag-shrunk`/`-split`, the `bookstore-rag-alias` alias, and the `bookstore_analyst` / `bookstore_read_only` security objects. If you ran one of those revisions, delete them individually — a `404` means they're already gone. They may also have left `persistent`/`transient` cluster-setting overrides (awareness, watermarks, backpressure); check with `GET _cluster/settings?flat_settings=true` and `null` out anything left.

```http
DELETE _plugins/_ism/policies/bookstore-searches-policy
```

**Fast mode** — `68-cleanup-delete-indexes.bru` → `69-cleanup-delete-ism.bru`

## What you learned

- **5-1:** shard sizing math, the yellow-cluster failure mode and its fix, `_cat/allocation` + `allocation/explain` triage, with awareness and disk watermarks as reference.
- **5-2:** `index:false` / `enabled:false` mappings, the write-alias → rollover → ISM lifecycle, with the shrink + alias-swap recipe as reference.
- **5-3:** `on_disk` vs `in_memory`, `compression_level`, and correct **fp16 scalar quantization** via the Faiss `sq` encoder.
- **5-4:** the monitoring loop (health, nodes, heap), with least-privilege security as reference.
- **5-5:** request caching, `_profile`, and slow logs hands-on, with priority routing and search backpressure as reference.

## Course wrap-up

That's the end of the course — congratulations. Looking back across the five chapters, you built the full arc of a production vector-search system:

1. **Chapter 1** — vector fundamentals: kNN indexes, HNSW vs IVF, quantization and `on_disk` mode, and the cost/performance levers (shards, segments, memory) that everything else builds on.
2. **Chapter 2** — the neural search pipeline: registering and deploying an embedding model in ML Commons, ingest pipelines that embed at index time, and semantic queries with the `neural` clause.
3. **Chapter 3** — beyond dense-only: neural sparse encoding, then hybrid search with score normalization, and RRF as the tuning-free alternative — with a side-by-side comparison of all four rankings.
4. **Chapter 4** — RAG in practice: a chunked, filtered, hybrid-searched bookstore index, cache warming and preload, and exposing the cluster to AI agents through the built-in MCP server.
5. **Chapter 5** — running it in production: shard sizing, allocation awareness, storage-mode trade-offs, least-privilege security, and the monitoring and backpressure levers that keep it healthy.

**Where to go next:**

- Re-run the labs against **your own dataset** — build a bulk body from your documents (like the ones in `rest/bulk/`) and re-use the Chapter 2 ingest pipeline as-is.
- Explore the [OpenSearch documentation](https://docs.opensearch.org/latest/) for the features this course touched as reference-only (TLS, audit logging, cross-cluster replication).
- Keep your trial cluster tidy: run each chapter's **Cleanup** section, or delete the cluster from the Instaclustr console when you're done.

