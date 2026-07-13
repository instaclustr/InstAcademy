← [Chapter 4](../Chapter%204/README.md)

# Chapter 5 — Production optimizations for OpenSearch clusters

You spent four chapters making vector search fast. This final chapter is about keeping it that way in production, where data outgrows its shard plan, clusters go yellow, memory gets tight, and the query that was instant in the demo becomes the slow one at peak traffic.

Consider this workshop your operations playbook. You will break a cluster on purpose and triage it back to health, design an index mapping that never needs rescuing, hand routine index chores to ISM so nobody babysits rollovers, cut vector memory in half with fp16 quantization, and close with the measurement tools (request caching, query profiling, slow logs) that show where query time actually goes.

Along the way, a handful of production patterns (shard-count math, allocation awareness, the shrink recipe, search backpressure) appear as read-along references: worth knowing, but not worth in the scope of demonstrating in this lab. Everything else runs live on your **Instaclustr trial cluster**.

---

## Lesson 5-1 — Shards: optimizing, merging, and shard balancing

You have been creating shards since Chapter 1, so this lesson skips the definitions and goes straight to the operations questions: how many shards, how big, and what to do when allocation breaks. The sizing tension is the part that only shows up at scale: too many small shards drown the coordinator in overhead, too few large ones slow recovery and limit flexibility. Aim for **10–50 GB per shard** (many teams target 20–30 GB).

### Step 1: Create a deliberately over-sharded index and watch the cluster go yellow

The best way to learn cluster triage is to break a cluster you're allowed to break. In this step you deliberately create the most common allocation failure in the wild: asking for more shard *copies* than there are data nodes to hold them. A node will never host both a primary and its own replica (that would defeat the point of a replica), so the extra copies simply have nowhere to go, they sit unassigned, and the cluster turns **yellow**. You'll see the symptom now and fix it in Step 2.

**Request**

```http
PUT my-index
{
  "settings": {
    "number_of_shards": 6,
    "number_of_replicas": 3
  }
}
```

**Expected** output:

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "my-index"
}
```

Then check cluster health. **Yellow** means there are unassigned replicas (data intact, redundancy lost). **Red** means a primary is missing (data unsearchable):

```http
GET _cluster/health
```

**Expected** `"status": "yellow"` with `"unassigned_shards" > 0`.

```json
{
  "cluster_name": "********",
  "status": "yellow",
  "timed_out": false,
  "number_of_nodes": 7,
  "number_of_data_nodes": 3,
  "discovered_master": true,
  "discovered_cluster_manager": true,
  "active_primary_shards": 20,
  "active_shards": 49,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 6,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 89.0909090909091
}
```

Why exactly 6 unassigned_shards? in the previous step we set the number of shards to 6 and replicas to 3, but a node will never hold two copies of the same shard, and there are only 3 data nodes. And with `relocating_shards` and `initializing_shards` both at 0, the cluster isn't still working on it. It has settled: those replicas *cannot* allocate until something changes. Step 2 changes it.

**Fast mode** — `06-delete-my-index-overshard.bru` → `07-create-oversharded-index.bru` → `08-cluster-health-before.bru`

### Step 2: Reduce replicas to fix allocation, then verify

Now play the role of an on-call engineer and bring the cluster back to green. Since the problem is more replica copies than nodes to hold them, the fix is to lower `number_of_replicas`. Note that replica count is a **live** setting: one API call, no reindex, and the cluster heals in seconds. 

**Request**

```http
PUT my-index/_settings
{
  "number_of_replicas": 0
}
```
**Expected** output:

```json
{
  "acknowledged": true
}
```

Now we need to verify the cluster health and the shard list.

***Request***

```http
GET _cluster/health
```

**Expected** `"status": "green"`, `"unassigned_shards": 0`

```json
{
  "cluster_name": "********",
  "status": "green",
  "timed_out": false,
  "number_of_nodes": 7,
  "number_of_data_nodes": 3,
  "discovered_master": true,
  "discovered_cluster_manager": true,
  "active_primary_shards": 20,
  "active_shards": 37,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 0,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 100
}
```

As you can see, by fixing the replica overallocation our cluster immediately went back to a green health state.

**Fast mode** — `09-set-replicas-zero.bru` → `10-cluster-health-after.bru` → `11-cat-shards-unassigned.bru`

### Step 3: Diagnose allocation: per-node disk and allocation explain

You fixed this incident because you caused it and knew the answer. Real incidents don't come with an explanation attached, so meet the two tools that provide one. `_cat/allocation` shows how full each node's disk is, which matters because unassigned shards in production are very often a disk problem in disguise. And `allocation/explain` is the closest thing OpenSearch has to a "why" button: it returns plain-language, per-node decisions for exactly why a shard can or cannot allocate (out of disk, awareness violation, filtered out, and so on). Learn this pair now and your next 3 a.m. yellow cluster becomes a five-minute diagnosis.

**Request**

```http
GET _cat/allocation?v&h=node,disk.percent,disk.avail
```

**Expected** output: ~1% disk space utilized.

```
node           disk.percent disk.avail
ip-10-2-123-11            1     28.7gb
ip-10-2-37-236            1     28.7gb
ip-10-2-181-70            1     28.7gb
```

**Request**

```http
GET _cluster/allocation/explain
{
  "index": "my-index",
  "shard": 1,
  "primary": true
}
```

**Expected** output: you're asking about a healthy, started shard, so the API answers a different question than it would in an incident. Instead of "why is this shard stuck," it reports "is this shard where it should be".

Reading it top to bottom: `current_state: started` and `current_node` tell you shard 1's primary lives on one specific data node. `can_remain_on_current_node: yes` means no decider wants to evict it. And `can_rebalance_to_other_node: no` is not a problem to fix; it's the cluster saying a move would help nothing. The `node_allocation_decisions` list makes that concrete: each remaining data node answers `worse_balance`, meaning it *could* hold this shard, but taking it would make the cluster less balanced, not more. A healthy answer on every line.

```json
{
  "index": "my-index",
  "shard": 1,
  "primary": true,
  "current_state": "started",
  "current_node": {
    "id": "F9CA3Sq3ReSvZdflXArfzA",
    "name": "ip-10-2-181-70",
    "transport_address": "10.2.181.70:9300",
    "attributes": {
      "rack_id": "us-west-2c",
      "shard_indexing_pressure_enabled": "true"
    },
    "weight_ranking": 1
  },
  "can_remain_on_current_node": "yes",
  "can_rebalance_cluster": "yes",
  "can_rebalance_to_other_node": "no",
  "rebalance_explanation": "cannot rebalance as no target node exists that can both allocate this shard and improve the cluster balance",
  "node_allocation_decisions": [
    {
      "node_id": "w5pYbppFT6-lxuh62xqkmw",
      "node_name": "ip-10-2-37-236",
      "transport_address": "10.2.37.236:9300",
      "node_attributes": {
        "rack_id": "us-west-2a",
        "shard_indexing_pressure_enabled": "true"
      },
      "node_decision": "worse_balance",
      "weight_ranking": 1
    },
    {
      "node_id": "SEDgR4UkS96_RaYdAdJMMw",
      "node_name": "ip-10-2-123-11",
      "transport_address": "10.2.123.11:9300",
      "node_attributes": {
        "rack_id": "us-west-2b",
        "shard_indexing_pressure_enabled": "true"
      },
      "node_decision": "worse_balance",
      "weight_ranking": 2
    }
  ]
}
```

**Fast mode** — `12-cat-allocation-disk.bru` → `13-allocation-explain.bru`

---

## Lesson 5-2 — Index optimization for performance and storage efficiency

Nearly every index setting you have touched this course was decided at creation time, and that is the real lesson here: mapping and shard choices are effectively permanent once documents land. This lesson is about making those one-shot decisions deliberately, then automating everything that happens after. You will create a mapping that only indexes the fields you actually search, then set up an ISM policy so rollover and cleanup happen automatically instead of by hand. This lesson also includes a read-along shrink recipe, which shows how to reduce the shard count on an existing index if you sized it wrong.

### Step 4: Create `my-index` with an optimized mapping, then read it back

You know from the videos that unindexed fields are cheaper; this mapping is what that looks like in practice. Most fields get the exact types you'd expect by now (`keyword` for identifiers and filters, `text` for search). Two fields opt out of indexing. `internal_notes` sets **`index: false`** because staff read it but nobody searches it. `inventory_metadata` sets **`enabled: false`**, which skips indexing the object and all of its sub-fields, because the application only ever retrieves it and never queries it. Decide this when you design the index, because making a field searchable later means a reindex. This step also recreates `my-index` as a clean single-shard index for the lifecycle demos ahead.

**Request** - Delete the current index

```http
DELETE my-index
```

**Expected** Output:
```json
{
  "acknowledged": true
}
```

**Request** - Build a new index with optimized mapping

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
**Expected** output:

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "my-index"
}
```

**Fast mode** — `16-delete-my-index-mapping.bru` → `17-create-my-index-bookstore.bru` → `18-get-mapping.bru`

### Step 5: Bulk sample documents into `my-index`

Ten documents and one refresh. The caching, profiling, and slow-log work in Lesson 5-4 all runs against this index, and those demos are more convincing with real data behind them. Notice that every document fills in the two opt-out fields from Step 4. Want to see the opt-outs work after the load? We'll search `internal_notes` for any word from a note and you'll get zero hits, then fetch any document by id (`GET my-index/_doc/978-0143127740`) and both fields are sitting right there in `_source`. Stored for reading, invisible to search, exactly as designed.

**Request** - Load data into our index

```http
POST _bulk
{ "index": { "_index": "my-index", "_id": "978-0143127740" } }
{ "book_id": "978-0143127740", "isbn": "978-0143127740", "title": "The Martian", "author": "Andy Weir", "genre": "Science Fiction", "description": "An astronaut stranded on Mars fights to survive.", "price": 16.99, "in_stock": true, "published_year": 2014, "internal_notes": "Perennial staff pick; keep face-out on the sci-fi endcap.", "inventory_metadata": { "warehouse": "PDX-1", "aisle": "12A", "last_counted": "2026-06-28" } }
{ "index": { "_index": "my-index", "_id": "978-0307277677" } }
{ "book_id": "978-0307277677", "isbn": "978-0307277677", "title": "The Road", "author": "Cormac McCarthy", "genre": "Fiction", "description": "A father and son journey through a post-apocalyptic landscape.", "price": 15.95, "in_stock": true, "published_year": 2006, "internal_notes": "Assign to the book-club table in October.", "inventory_metadata": { "warehouse": "PDX-1", "aisle": "03C", "last_counted": "2026-06-28" } }
{ "index": { "_index": "my-index", "_id": "978-0593135204" } }
{ "book_id": "978-0593135204", "isbn": "978-0593135204", "title": "Project Hail Mary", "author": "Andy Weir", "genre": "Science Fiction", "description": "A lone astronaut wakes with no memory and must save Earth from an extinction-level threat.", "price": 18.99, "in_stock": true, "published_year": 2021, "internal_notes": "Customers who liked The Martian ask for this; shelve nearby.", "inventory_metadata": { "warehouse": "PDX-2", "aisle": "12B", "last_counted": "2026-07-01" } }
{ "index": { "_index": "my-index", "_id": "978-0441172719" } }
{ "book_id": "978-0441172719", "isbn": "978-0441172719", "title": "Dune", "author": "Frank Herbert", "genre": "Science Fiction", "description": "A young nobleman is drawn into a war for a desert planet and its spice.", "price": 19.99, "in_stock": true, "published_year": 1965, "internal_notes": "Movie tie-in cover sells faster than the classic cover.", "inventory_metadata": { "warehouse": "PDX-2", "aisle": "11A", "last_counted": "2026-05-19" } }
{ "index": { "_index": "my-index", "_id": "978-0307588371" } }
{ "book_id": "978-0307588371", "isbn": "978-0307588371", "title": "Gone Girl", "author": "Gillian Flynn", "genre": "Mystery", "description": "A wife disappears and a marriage's secrets unravel under investigation.", "price": 14.99, "in_stock": false, "published_year": 2012, "internal_notes": "Restock delayed; distributor backorder until August.", "inventory_metadata": { "warehouse": "PDX-1", "aisle": "07D", "last_counted": "2026-06-30" } }
{ "index": { "_index": "my-index", "_id": "978-0307454546" } }
{ "book_id": "978-0307454546", "isbn": "978-0307454546", "title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "genre": "Mystery", "description": "A journalist and a hacker investigate a decades-old disappearance.", "price": 16.95, "in_stock": true, "published_year": 2008, "internal_notes": "Series sells as a set; bundle with volumes 2 and 3.", "inventory_metadata": { "warehouse": "PDX-3", "aisle": "08A", "last_counted": "2026-06-15" } }
{ "index": { "_index": "my-index", "_id": "978-0399590504" } }
{ "book_id": "978-0399590504", "isbn": "978-0399590504", "title": "Educated", "author": "Tara Westover", "genre": "Memoir", "description": "A memoir of leaving a survivalist family for a university education.", "price": 17.99, "in_stock": true, "published_year": 2018, "internal_notes": "Frequent gift purchase; keep near the register in December.", "inventory_metadata": { "warehouse": "PDX-1", "aisle": "21B", "last_counted": "2026-07-02" } }
{ "index": { "_index": "my-index", "_id": "978-1250301697" } }
{ "book_id": "978-1250301697", "isbn": "978-1250301697", "title": "The Silent Patient", "author": "Alex Michaelides", "genre": "Thriller", "description": "A psychotherapist becomes obsessed with a patient who refuses to speak.", "price": 13.99, "in_stock": true, "published_year": 2019, "internal_notes": "Demand spike from social media; reorder threshold raised to 12.", "inventory_metadata": { "warehouse": "PDX-2", "aisle": "07A", "last_counted": "2026-06-25" } }
{ "index": { "_index": "my-index", "_id": "978-0735219090" } }
{ "book_id": "978-0735219090", "isbn": "978-0735219090", "title": "Where the Crawdads Sing", "author": "Delia Owens", "genre": "Fiction", "description": "An abandoned girl raises herself in the marshes of North Carolina.", "price": 15.99, "in_stock": false, "published_year": 2018, "internal_notes": "Damaged shipment returned; awaiting replacement stock.", "inventory_metadata": { "warehouse": "PDX-3", "aisle": "04C", "last_counted": "2026-06-20" } }
{ "index": { "_index": "my-index", "_id": "978-0547928227" } }
{ "book_id": "978-0547928227", "isbn": "978-0547928227", "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "description": "A homebody hobbit is swept into a quest to reclaim a dwarven kingdom.", "price": 14.95, "in_stock": true, "published_year": 1937, "internal_notes": "Evergreen seller; never let stock drop below 6.", "inventory_metadata": { "warehouse": "PDX-1", "aisle": "10A", "last_counted": "2026-06-28" } }

```

**Expected** `"errors": false`, documents can be seen in the `items` array

```json
{
  "took": 44,
  "errors": false,
  "items": [
    {
      "index": {
        "_index": "my-index",
        "_id": "978-0143127740",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 1,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 0,
        "_primary_term": 1,
        "status": 201
      }
    },[...]
```

**Request** - Refresh the index

```http
POST my-index/_refresh
```

**Expected** `_shards.successful: 1`. All ten documents are now searchable.

```json
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  }
}
```

**Fast mode** — `20-bulk-my-index.bru` → `21-refresh-my-index.bru`

### Step 6: Automate the index lifecycle: write alias, rollover, and ISM

Data like logs, metrics, and search history never stops arriving. If it all lands in one index, that index grows forever. The standard fix has three parts. You create a **time-based index** (`searches-000001`) with a **write alias** (`is_write_index: true`); your application writes to the alias and never needs to know which physical index is active. You call `_rollover`, which creates the next index and moves the write alias whenever the active index gets too old, too big, or too full. And you attach an **ISM policy** so the cycle repeats automatically instead of relying on someone to remember it. Aging out old data then becomes simple: delete a whole retired index, which is much cheaper than a delete-by-query. One ordering detail matters before you start: `ism_template` only attaches to indexes created *after* the policy exists, so in this step the policy comes first.

**Request** — create the lifecycle policy. The `min_doc_count: 5` rollover threshold is deliberately tiny so you can watch it fire in the next few requests; production values look more like `min_index_age: 30d` or `min_size: 50gb`.

```http
PUT _plugins/_ism/policies/bookstore-searches-policy
{
  "policy": {
    "description": "Demo: roll over at 5 docs, delete after 90 days",
    "default_state": "hot",
    "states": [
      {
        "name": "hot",
        "actions": [ { "rollover": { "min_doc_count": 5 } } ],
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

**Expected** an `_id` of `bookstore-searches-policy` and the policy echoed back, with retry defaults filled in on the rollover action.

```json
{
  "_id": "bookstore-searches-policy",
  "_version": 1,
  "_primary_term": 1,
  "_seq_no": 6605,
  "policy": {
    "policy": {
      "policy_id": "bookstore-searches-policy",
      "description": "Demo: roll over at 5 docs, delete after 90 days",
      [...]
     
```

**Request** — Next we'll create the first backing index with the write alias. The extra setting tells ISM which alias its rollover action should move; in production an index template would stamp it onto every `searches-*` index automatically.

```http
PUT searches-000001
{
  "settings": { "index.plugins.index_state_management.rollover_alias": "searches-current" },
  "aliases": { "searches-current": { "is_write_index": true } }
}
```

**Expected** output:

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "searches-000001"
}
```

Now let's check that the policy attached on its own:

```http
GET _plugins/_ism/explain/searches-000001
```

**Expected** output (attachment happens within a few seconds of index creation; if `policy_id` is still `null`, run it again):

```json
{
  "searches-000001": {
    "index.plugins.index_state_management.policy_id": "bookstore-searches-policy",
    "index.opendistro.index_state_management.policy_id": "bookstore-searches-policy",
    "index": "searches-000001",
    "index_uuid": "qvwrmT74Qtm5Xqw8LGwd3Q",
    "policy_id": "bookstore-searches-policy",
    "enabled": true
  },
  "total_managed_indices": 1
}
```

Nobody registered this index with ISM by hand. It matched the `searches-*` pattern at creation time, and the policy picked it up.

**Request** — Next we'll write six search-history events through the alias. The `refresh=true` makes them count toward the rollover condition immediately.

```http
POST _bulk?refresh=true
{ "index": { "_index": "searches-current" } }
{ "query": "mystery novels under 20 dollars", "results": 14, "timestamp": "2026-07-13T09:14:02Z" }
{ "index": { "_index": "searches-current" } }
{ "query": "andy weir new releases", "results": 3, "timestamp": "2026-07-13T09:15:47Z" }
{ "index": { "_index": "searches-current" } }
{ "query": "books like project hail mary", "results": 9, "timestamp": "2026-07-13T09:16:29Z" }
{ "index": { "_index": "searches-current" } }
{ "query": "cormac mccarthy the road", "results": 1, "timestamp": "2026-07-13T09:18:03Z" }
{ "index": { "_index": "searches-current" } }
{ "query": "fantasy classics for beginners", "results": 22, "timestamp": "2026-07-13T09:21:11Z" }
{ "index": { "_index": "searches-current" } }
{ "query": "memoirs about education", "results": 6, "timestamp": "2026-07-13T09:24:55Z" }
```

**Expected** `"errors": false`. Look at any item in the response: `"_index": "searches-000001"`. You wrote to the alias, and OpenSearch resolved the physical index for you.

```json
{
  "took": 536,
  "errors": false,
  "items": [
    {
      "index": {
        "_index": "searches-000001",
        "_id": "hBuHXZ8BCKwDOnnOt0DM",
        "_version": 1,
        "result": "created",
        "forced_refresh": true,
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 0,
        "_primary_term": 1,
        "status": 201
      }
    },[...]
}
```

**Request** — now trigger the rollover. This call asks OpenSearch to check the index behind `searches-current` against the conditions in the body, and if any condition is met, to create the next index and move the write alias onto it. You loaded six documents and the condition says five, so the check will pass. OpenSearch reads the `-000001` suffix and names the new index `searches-000002` on its own. This is the same operation ISM runs on its schedule; you are running it by hand so you don't have to wait for the next check.

```http
POST searches-current/_rollover
{ "conditions": { "max_docs": 5 } }
```

**Expected** output:

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "old_index": "searches-000001",
  "new_index": "searches-000002",
  "rolled_over": true,
  "dry_run": false,
  "conditions": {
    "[max_docs: 5]": true
  }
}
```

`"rolled_over": true` is the confirmation that it happened. `conditions` shows the check that justified it (six documents met the `max_docs: 5` threshold), and `old_index` / `new_index` name the index that stopped receiving writes and the one that now does. Confirm that by looking at the alias:

```http
GET _alias/searches-current
```

**Expected** output:

```json
{
  "searches-000001": {
    "aliases": {
      "searches-current": {
        "is_write_index": false
      }
    }
  },
  "searches-000002": {
    "aliases": {
      "searches-current": {
        "is_write_index": true
      }
    }
  }
}
```

This is the whole pattern on one screen. The application never stopped writing to `searches-current`, but new documents now land in `searches-000002`, while the old data in `searches-000001` stays searchable through the same alias. And because `searches-000002` matches the `ism_template` pattern too, it is already managed; run the explain request against it if you want proof. In production you don't run the rollover call yourself: ISM checks its managed indexes about every five minutes and runs this same rollover when a condition is met. You triggered it manually only so you didn't have to sit and wait. The delete phase works the same way, just on a 90-day clock.

**Fast mode** — `35-create-ism-policy.bru` → `36-create-searches-index.bru` → `37-ism-explain.bru` → `38-bulk-search-events.bru` → `39-rollover-searches.bru` → `40-get-alias-searches.bru`

---

## Lesson 5-3 — Optimizing for vector storage and search

Vectors are memory hogs by design. A 768-dim `float` vector is `768 × 4 = 3072` bytes; the HNSW graph that makes search fast must live in RAM. Bookstore math: `500k books × 768-dims × 4 bytes ≈ 1.5 GB` raw, and `≈ 2.25 GB` with ~50% HNSW overhead, which is fine in one shard. At 10M books that's ~45 GB and must be spread across shards/nodes. Two escape hatches when memory is the constraint: **`on_disk` mode** and **scalar quantization (fp16)**.

### Step 7: Cut memory in half with fp16 scalar quantization

If someone offered to cut your vector memory bill in half for under 1% recall loss, you'd probably almost always take that tradeoff, and that's exactly what fp16 quantization is. Each dimension is stored as a 16-bit float instead of 32, dropping our bookstore shard math from ~2.25 GB to ~1.1 GB. One correction to the video script before you run it: `data_type: "float16"` does not exist in OpenSearch. The real mechanism is a **Faiss scalar-quantization encoder**, set via `method.parameters.encoder = { "name": "sq" }`. Values must fit within `[-65504, 65504]`, which normalized embeddings always do.

**Request** — this is the same FAISS HNSW recipe you used for `bookstore-rag` in Chapter 4: 768 dimensions, `l2` distance, `m: 16`, `ef_construction: 128`. Read it looking for what changed and you'll find exactly one new line, the `encoder`. That line tells FAISS to store every vector dimension as a 16-bit float instead of a 32-bit one. Everything else about working with the index (queries, bulk loads, warmup) stays exactly the same.

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

**Expected** output:

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "book-embeddings-fp16"
}
```

An acknowledgment alone doesn't prove the quantization is on, so read the mapping back and look inside `method.parameters`:

```http
GET book-embeddings-fp16/_mapping
```

**Expected** output: the `encoder` block is there. From this point on, every vector written to this index gets stored as fp16 on arrival, at half the memory of the 32-bit default. If you had misspelled the encoder name, the create would have failed loudly, so what you're really confirming here is that you created the index you think you did before data starts landing in it.

```json
{
  "book-embeddings-fp16": {
    "mappings": {
      "properties": {
        "embedding": {
          "type": "knn_vector",
          "dimension": 768,
          "method": {
            "engine": "faiss",
            "space_type": "l2",
            "name": "hnsw",
            "parameters": {
              "ef_construction": 128,
              "encoder": {
                "name": "sq",
                "parameters": {}
              },
              "m": 16
            }
          },
          "space_type": "l2"
        }
      }
    }
  }
}
```

**Request** — now build the experiment that proves the memory claim. This second index is the control group: the identical mapping with the encoder line removed, so every byte of difference you measure in Step 8 comes from quantization and nothing else.

```http
PUT book-embeddings-float
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
            "ef_construction": 128,
            "m": 16
          }
        }
      }
    }
  }
}
```

**Expected** `"acknowledged": true`, `"index": "book-embeddings-float"`.

**Request** — load the same vectors into both indexes. The bulk file ([`rest/bulk/chapter-5-embeddings-compare.ndjson`](../../rest/bulk/chapter-5-embeddings-compare.ndjson)) holds 50 pre-generated 768-dimensional vectors and writes each one twice, once per index, so the two indexes end up holding identical data. Paste its contents after the `POST` line, then force-merge so each index settles into one segment and the comparison is clean.

```http
POST _bulk?refresh=true
{ /* paste the contents of chapter-5-embeddings-compare.ndjson */ }
```

```http
POST book-embeddings-float,book-embeddings-fp16/_forcemerge?max_num_segments=1
```

**Expected** bulk `"errors": false` with 100 items (50 documents into each index), every item showing `"result": "created"` and status `201`. The force-merge returns `{"_shards": {"total": 4, "successful": 4, "failed": 0}}`: four shard copies touched, one primary and one replica per index. Both indexes now hold the same 50 vectors; the only difference between them is how the HNSW graph stores each dimension. Step 8 measures what that difference costs.

**Fast mode** — `45-create-fp16-quantized.bru` → `46-get-fp16-mapping.bru` → `47-create-float-control.bru` → `48-bulk-embeddings-compare.bru` → `49-forcemerge-embeddings.bru`

### Step 8: Measure what fp16 actually saves

A claim like "half the memory" deserves verification, and you just built the perfect experiment for it: two indexes, identical data, one encoder line apart. Two measurements settle it. Disk first, using `_stats`. Its raw response is enormous (hundreds of counters covering indexing, search, merges, and caches), so keep the `filter_path` habit from Chapter 3 and ask only for the numbers that answer the cost question.

**Request**

```http
GET book-embeddings-float,book-embeddings-fp16/_stats?filter_path=indices.*.primaries.docs.count,indices.*.primaries.store.size_in_bytes
```

**Expected** output:

```json
{
  "indices": {
    "book-embeddings-fp16": {
      "primaries": {
        "docs": {
          "count": 50
        },
        "store": {
          "size_in_bytes": 244886
        }
      }
    },
    "book-embeddings-float": {
      "primaries": {
        "docs": {
          "count": 50
        },
        "store": {
          "size_in_bytes": 321626
        }
      }
    }
  }
}
```

Same 50 documents, but fp16 is only about 24% smaller on disk, not half. That is not a failure; it's the design. Lucene keeps a full-precision copy of every vector on disk (used for exact scoring and rebuilding), and quantization never touches it. The part that shrank by half is the FAISS graph file, and the graph file is the only part that loads into memory for search. (Want to see the full-precision copy? Re-run with `&include_segment_file_sizes=true`: the `vec` file is 153,708 bytes in both indexes, byte-identical.) So disk tells half the story. The real question is what sits in RAM, and the k-NN plugin can answer it because the graphs aren't loaded until an index is warmed or searched.

**Request** — check graph memory before warming anything:

```http
GET _plugins/_knn/stats?stat=graph_memory_usage&filter_path=nodes.*.graph_memory_usage
```

**Expected** every node reports `0`. Nothing has searched these indexes yet, so no graph is in memory. (If other k-NN indexes on your cluster have been warmed or searched, your baseline is higher; watch the increments instead of the absolute numbers.)

**Request** — load the float graph into memory, then measure again:

```http
GET _plugins/_knn/warmup/book-embeddings-float
```

```http
GET _plugins/_knn/stats?stat=graph_memory_usage&filter_path=nodes.*.graph_memory_usage
```

**Expected** two nodes now report `157` each (the value is in KB). That's the full-precision graph, loaded once for the primary and once for the replica, on whichever two data nodes hold them.

**Request** — now the fp16 graph:

```http
GET _plugins/_knn/warmup/book-embeddings-fp16
```

```http
GET _plugins/_knn/stats?stat=graph_memory_usage&filter_path=nodes.*.graph_memory_usage
```

**Expected** output: the totals grow by `82` per fp16 shard copy. Your node names and shard placement will differ, but the arithmetic is the same: four graph copies in memory, `157 + 157` for float and `82 + 82` for fp16. On this cluster one node happened to hold a copy of each, so it reports `239`:

```json
{
  "nodes": {
    "SEDgR4UkS96_RaYdAdJMMw": {
      "graph_memory_usage": 157
    },
    "BnNel5ARRiCjRTNHxNIFGQ": {
      "graph_memory_usage": 0
    },
    "cK0uLQjwTuyTO00iydQ3vg": {
      "graph_memory_usage": 0
    },
    "w5pYbppFT6-lxuh62xqkmw": {
      "graph_memory_usage": 239
    },
    "qn_icf3PSH-5-yV_StCi6g": {
      "graph_memory_usage": 0
    },
    "8juFfT-sRfW__kvz6NbgOA": {
      "graph_memory_usage": 0
    },
    "F9CA3Sq3ReSvZdflXArfzA": {
      "graph_memory_usage": 82
    }
  }
}
```

There is the proof: 157 KB per copy for the float graph, 82 KB for fp16, measured on your own cluster with identical data. Scale that ratio up to the lesson intro's bookstore math (about 2.25 GB of graph per shard at 500k books) and it's the difference between fitting in your data nodes' RAM and not. The takeaway worth keeping: quantization buys you memory, not disk. Know which resource a knob buys before you reach for it.

**Fast mode** — `50-compare-store-stats.bru` → `51-knn-graph-memory.bru` → `52-warmup-float.bru` → re-run `51` → `53-warmup-fp16.bru` → re-run `51`

---

## Lesson 5-4 — Mastering OpenSearch query optimization

Under peak load, all queries competing equally means a checkout can stall behind hundreds of "show me mystery novels." OpenSearch has no per-query priority queue, but you can approximate one with **index/hardware separation**, **request caching**, **recovery priority**, and **search backpressure**. You can also **profile** slow queries and log them.

### Step 9: Enable shard request caching

Think about how much of your search traffic is the *same* few requests fired over and over: current prices, order status, the dashboard someone keeps refreshing. Recomputing those from scratch every time is pure waste. The shard request cache stores the results of aggregation and `size: 0` queries at the shard level, so hot, repeated requests get answered from memory while the cluster's compute goes to queries that are genuinely new. Enable it per index, and note the practical effect: your highest-value, most-hammered shards end up staying cached the longest. We use the populated `my-index` from Lesson 5-2.

**Request** — turn the cache on for the index.

```http
PUT my-index/_settings
{
  "index.requests.cache.enable": true
}
```

**Expected** `{"acknowledged": true}`.

**Request** — now run a cacheable search, twice. Not every request can be cached: the shard request cache only stores `size: 0` responses, which is counts and aggregations, exactly the dashboard-style traffic that repeats all day. The `?request_cache=true` parameter asks for caching explicitly on this request. Run it two times in a row and watch the `took` value.

```http
GET my-index/_search?request_cache=true
{
  "size": 0,
  "query": { "match_all": {} }
}
```

**Expected** output: the first run computes the answer (`"took": 2` on this cluster); the second run is served from the cache (`"took": 0`). The rest of the response is identical both times:

```json
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

The query matched all ten documents, so the response reports `"hits.total.value": 10`. But because the request asked for `size: 0`, no actual documents come back; the `hits` array stays empty. Count-only responses like this one are exactly what the shard request cache stores.

**Request** — prove the cache did the work by reading its counters:

```http
GET my-index/_stats/request_cache?filter_path=_all.total.request_cache
```

**Expected** output:

```json
{
  "_all": {
    "total": {
      "request_cache": {
        "memory_size_in_bytes": 689,
        "evictions": 0,
        "hit_count": 1,
        "miss_count": 1
      }
    }
  }
}
```

One miss and one hit: the first search had to compute the result and store it (those are the 689 bytes), and the second search was answered from memory without touching the shard. The counters are cumulative, so every extra re-run adds a hit. And you never trade correctness for this speed: the cache invalidates automatically whenever the shard refreshes with new data, so it cannot serve stale results.

**Fast mode** — `59-enable-request-cache.bru` → `60-cacheable-search.bru` (run it twice) → `61-request-cache-stats.bru`

### Step 10: Profile a query

Never optimize a slow query on a hunch. Adding `"profile": true` to any search returns a per-shard, per-component timing breakdown, showing exactly which clause, rewrite, or collector is eating the time, so you fix the actual bottleneck instead of the suspected one. Make it the first move whenever someone reports "search is slow."

**Request** — add `"profile": true` to the search body. One warning: profiling is verbose. Even this trivial query returns about 10 KB of per-component timings, so the `filter_path` below keeps only the three numbers you triage with. (When you profile for real, drop the `filter_path` and dig into the full breakdown once you know which component to blame.)

```http
GET my-index/_search?filter_path=took,profile.shards.searches.query.type,profile.shards.searches.query.description,profile.shards.searches.query.time_in_nanos,profile.shards.searches.rewrite_time,profile.shards.searches.collector
{
  "profile": true,
  "query": { "match_all": {} }
}
```

**Expected** output:

```json
{
  "took": 42,
  "profile": {
    "shards": [
      {
        "searches": [
          {
            "query": [
              {
                "type": "ApproximateScoreQuery",
                "description": "ApproximateScoreQuery(originalQuery=*:*, approximationQuery=Approximate(*:*))",
                "time_in_nanos": 37924
              }
            ],
            "rewrite_time": 12398,
            "collector": [
              {
                "name": "TopScoreDocCollector",
                "reason": "search_top_hits",
                "time_in_nanos": 17657
              }
            ]
          }
        ]
      }
    ]
  }
}
```

Read the three numbers, remembering they are nanoseconds: the query itself spent 38 microseconds matching and scoring, rewriting the query into its executable form took 12, and collecting the results took 18. All well under a tenth of a millisecond on ten documents, which is the point of learning the shape now: when a real query misbehaves, the slow component stands out in exactly these three fields. Two details worth noticing: the `description` shows what your query became internally (OpenSearch 3.x wraps `match_all` in its approximation framework, and the original `*:*` is visible inside), and `took` is milliseconds for the whole request while the profile numbers are nanoseconds per component, so they will not add up to `took`.

**Fast mode** — `62-profile-query.bru`

### Step 11: Configure slow logs (per index)

Profiling works when you already know which query is slow, but in production the pathological query usually strikes while nobody is watching. Slow logs are the tripwire: any query or fetch that exceeds your thresholds gets recorded to the node logs with its full body, so the evidence is waiting for you instead of vanished. These are **index-level** settings with separate query and fetch thresholds per severity, letting you decide per index what counts as "worryingly slow."

**Request** — set three thresholds on the index. The two `query` thresholds cover the search phase (finding and scoring matches) at different severities, and the `fetch` threshold covers the fetch phase (retrieving the actual documents). Fetch gets a tighter limit because retrieving already-identified documents should be fast; if fetch is slow, something is wrong with document size or disk, not query complexity.

```http
PUT my-index/_settings
{
  "index.search.slowlog.threshold.query.warn": "10s",
  "index.search.slowlog.threshold.query.info": "5s",
  "index.search.slowlog.threshold.fetch.warn": "1s"
}
```

**Expected** output:

```json
{
  "acknowledged": true
}
```

Then read the settings back to confirm all three thresholds landed where you expect:

```http
GET my-index/_settings?filter_path=*.settings.index.search.slowlog
```

**Expected** output:

```json
{
  "my-index": {
    "settings": {
      "index": {
        "search": {
          "slowlog": {
            "threshold": {
              "fetch": {
                "warn": "1s"
              },
              "query": {
                "warn": "10s",
                "info": "5s"
              }
            }
          }
        }
      }
    }
  }
}
```

The thresholds are armed, and nothing else visible happens, because no query against ten documents will take five seconds. That's the point of a tripwire: you set it and move on. In production the entries land in each node's log files with the full query body (on a managed cluster you reach them through your provider's log delivery). The real decision is where to set the thresholds: `info` low enough to catch slow drift early, and `warn` reserved for latencies you would want to be paged about.

**Fast mode** — `63-set-slow-logs.bru` → `64-get-slowlog-settings.bru`

---

## Chapter 5 wrap-up

Every step in this workshop followed the same pattern: make a claim, then make the cluster prove it. You watched a yellow cluster explain exactly why six replicas had nowhere to go. You read an allocation decision straight from the decider that made it. You saw a write alias move to a new index mid-rollover, confirmed ISM attached itself to an index nobody registered by hand, measured fp16 cutting graph memory from 157 KB to 82, and caught a cache hit in the counters. That habit is the real lesson of the chapter: production operations is measurement, not guesswork. When your future cluster misbehaves, ask it to explain itself. It usually will.

## What you learned

- **5-1:** shard sizing math, the yellow-cluster failure mode and its fix, `_cat/allocation` + `allocation/explain` triage, with awareness and disk watermarks as reference.
- **5-2:** `index:false` / `enabled:false` mappings, the write-alias → rollover → ISM lifecycle, with the shrink + alias-swap recipe as reference.
- **5-3:** `on_disk` vs `in_memory`, `compression_level`, and correct **fp16 scalar quantization** via the Faiss `sq` encoder.
- **5-4:** request caching, `_profile`, and slow logs hands-on, with priority routing and search backpressure as reference.

## Course wrap-up

That's the end of the course — congratulations. Looking back across the five chapters, you built the full arc of a production vector-search system:

1. **Chapter 1** — vector fundamentals: kNN indexes, HNSW vs IVF, quantization and `on_disk` mode, and the cost/performance levers (shards, segments, memory) that everything else builds on.
2. **Chapter 2** — the neural search pipeline: registering and deploying an embedding model in ML Commons, ingest pipelines that embed at index time, and semantic queries with the `neural` clause.
3. **Chapter 3** — beyond dense-only: neural sparse encoding, then hybrid search with score normalization, and RRF as the tuning-free alternative — with a side-by-side comparison of all four rankings.
4. **Chapter 4** — RAG in practice: a chunked, filtered, hybrid-searched bookstore index, cache warming and preload, and exposing the cluster to AI agents through the built-in MCP server.
5. **Chapter 5** — running it in production: shard sizing and yellow-cluster triage, the rollover + ISM lifecycle, measured fp16 memory savings, and the caching, profiling, and slow-log toolkit that keeps queries fast.

**Where to go next:**

- Re-run the labs against **your own dataset** — build a bulk body from your documents (like the ones in `rest/bulk/`) and re-use the Chapter 2 ingest pipeline as-is.
- Explore the [OpenSearch documentation](https://docs.opensearch.org/latest/) for the features this course touched as reference-only (the shrink recipe, allocation awareness, search backpressure).
- Keep your trial cluster tidy: run the **Cleanup** section below to remove this chapter's assets, or delete the cluster from the Instaclustr console when you're done.

You started this course pasting eight-dimensional toy vectors into an index to learn what a k-NN search even was. Five chapters later, you have deployed embedding models, built pipelines that chunk and embed documents on arrival, compared lexical, sparse, dense, and hybrid rankings on real books, tuned a RAG index end to end, opened your cluster to AI agents over MCP, and proved every optimization with a measurement instead of a promise. That is a production skill set. Point it at your own data next, and thanks for building along.

## Cleanup

Remove the lab indexes and policy.

```http
DELETE my-index,searches-000001,searches-000002,book-embeddings-float,book-embeddings-fp16
```


```http
DELETE _plugins/_ism/policies/bookstore-searches-policy
```

**Fast mode** — `68-cleanup-delete-indexes.bru` → `69-cleanup-delete-ism.bru`

