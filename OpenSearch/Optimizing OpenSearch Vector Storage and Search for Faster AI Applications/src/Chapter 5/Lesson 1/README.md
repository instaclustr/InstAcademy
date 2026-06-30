# Chapter 5 Lesson 1 — Shards, allocation, and cluster health

**InstAcademy → OpenSearch:** Lesson **5-1** · [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications](../../OpenSearch%20Learning%20Path%201.docx) — routing awareness, shard visibility, force merge, oversharding, replicas, and disk watermarks.

## Overview

### Goals

By the end of this lesson you will:

1. Configure **routing awareness** so shards spread across zones on a multi-node cluster.
2. Inspect **shard distribution** with `_cat/shards`.
3. **Force-merge** a loaded index to reduce Lucene segments.
4. Create an **oversharded** index and diagnose **yellow** cluster health.
5. Use **allocation explain** and adjust **replica** counts.
6. Review and set cluster **disk watermark** thresholds.

### Prerequisites

- Complete [Chapter 1 Lesson 1](../../Chapter%201/1-1/README.md) (cluster connectivity).
- Run [Chapter 4 Lesson 2](../../Chapter%204/Lesson%202/README.md) **`06-put-it-all-together.py`** (or equivalent) so **`bookstore-rag-all-together`** exists before **Step 3**.
- Open **OpenSearch Dashboards → Dev Tools** (or Bruno fast mode: [`bruno/Chapter 5/Lesson 1/`](../../../bruno/Chapter%205/Lesson%201/)).
- Use your **3-node Instaclustr trial cluster**. Routing-awareness settings in Step 1 only take effect when nodes advertise matching `node.attr.zone` values (see course video); on managed trials you can still run the API calls and observe behavior.

**Save values as you go:**

| After step | Save | Used for |
| --- | --- | --- |
| Step 4 | Index name **`my-index`** | Steps 5–6 |

---

## Lab steps

### **Step 1: Configure routing awareness**

**Why**  
Without awareness, the shard allocator balances only by count and disk. **Awareness** tries to keep a primary and its replica on nodes in *different* zones. **`force.zone.values`** blocks allocation until at least one node exists in each listed zone — preventing all replicas from piling into one surviving zone after a partial outage.

**Prerequisite:** each node must set `node.attr.zone=zoneN` in `opensearch.yml`. Without node attributes, this cluster setting has no effect.

**Request** — paste into Dev Tools:

```http
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.awareness.attributes": "zone",
    "cluster.routing.allocation.awareness.force.zone.values": "zone1,zone2,zone3"
  }
}
```

**Expected** `"acknowledged": true` in the response.

**Fast mode**  
`bruno/Chapter 5/Lesson 1/01-routing-awareness.bru`


### **Step 2: Inspect shard distribution**

**Why**  
After changing awareness, replicas, or allocation rules, confirm shards actually moved. Sorting by node makes it easy to spot uneven distribution or shards stuck in `UNASSIGNED` / `INITIALIZING`.

**Request** — paste into Dev Tools:

```http
GET _cat/shards?v&s=node&format=json
```

**Expected**  
JSON array of shard rows. Scan for:

- Roughly even shard counts per node on your 3-node cluster.
- `state: "STARTED"` on allocated shards.
- Primary and replica of the same shard on **different** nodes (when replicas > 0).

**Fast mode**  
`bruno/Chapter 5/Lesson 1/02-check-shard-distribution.bru`


### **Step 3: Force-merge an index**

**Why**  
Bulk indexing creates many Lucene segments. Search must visit every segment, so too many segments hurts query latency. Force merge compacts segments — run after large loads or on read-heavy indexes during a maintenance window.

**Prerequisite:** index **`bookstore-rag-all-together`** from Chapter 4 Lesson 2.

**Request** — paste into Dev Tools:

```http
POST bookstore-rag-all-together/_forcemerge?max_num_segments=5
```

**Expected** response includes `"_shards"` with successful shard counts. The operation can take minutes on a loaded index.

**When not to use:** during heavy writes, or on hot write indexes where Lucene's background merges are sufficient.

**Fast mode**  
`bruno/Chapter 5/Lesson 1/03-force-merge.bru`


### **Step 4: Create an oversharded index (deliberately bad)**

**Why**  
This demo shows what *not* to do. Six primaries × one replica = **12 shards** — far too many for a tiny dataset. On a small cluster, replicas may fail to allocate (a node cannot host both primary and replica of the same shard), turning the cluster **yellow**.

**Request** — paste into Dev Tools:

```http
DELETE my-index
```

A `404` is fine if the index did not exist.

```http
PUT my-index
{
  "settings": {
    "number_of_shards": 6,
    "number_of_replicas": 1
  }
}
```

**Expected** `"acknowledged": true`. Save the index name **`my-index`**.

**Fast mode**  
`bruno/Chapter 5/Lesson 1/04-index-too-many-shards.bru`


### **Step 5: Diagnose cluster health and fix replicas**

**Why**  
`_cluster/health` summarizes green/yellow/red status. When replicas cannot allocate, reducing `number_of_replicas` is a common lab fix (production clusters usually keep ≥ 1 replica for HA). **`_cluster/allocation/explain`** answers *why* a specific shard is unassigned.

### 5a — Health before

**Request** — paste into Dev Tools:

```http
GET _cluster/health
```

**Expected** `"status": "yellow"` (or `"red"`) with `"unassigned_shards" > 0` if replicas could not allocate.

### 5b — Set replicas to zero

**Request** — paste into Dev Tools:

```http
PUT my-index/_settings
{
  "number_of_replicas": 0
}
```

**Expected** `"acknowledged": true`.

### 5c — Health after

**Request** — paste into Dev Tools:

```http
GET _cluster/health
```

**Expected** `"status": "green"` once all primaries are started and unassigned count is 0.

### 5d — Shard details with unassigned reason

**Request** — paste into Dev Tools:

```http
GET _cat/shards?v&h=index,shard,prirep,state,node,unassigned.reason&format=json
```

**Expected** rows for **`my-index`** with `state: "STARTED"` and empty or node names in `node`.

### 5e — Per-node disk overview

**Request** — paste into Dev Tools:

```http
GET _cat/allocation?v&h=node,disk.used_percent,disk.avail&format=json
```

**Expected**  
disk usage per node — useful before tuning watermarks in Step 6.

### 5f — Allocation explain for one shard

**Request** — paste into Dev Tools:

```http
GET _cluster/allocation/explain
{
  "index": "my-index",
  "shard": 1,
  "primary": true
}
```

**Expected** JSON explaining which nodes were considered and why the shard was or was not allocated (`can_allocate`, `allocate_explanation`, per-node decisions).

**Fast mode**  
`bruno/Chapter 5/Lesson 1/05-cluster-health-and-replicas.bru`


### **Step 6: Configure disk watermarks**

**Why**  
Watermarks protect nodes from running out of disk:

- **low (85%)** — stop allocating *new* shards to the node.
- **high (90%)** — actively relocate shards away.
- **flood_stage (95%)** — indexes on the node go **read-only** to prevent corruption.

**Request** — paste into Dev Tools:

```http
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.disk.watermark.low": "85%",
    "cluster.routing.allocation.disk.watermark.high": "90%",
    "cluster.routing.allocation.disk.watermark.flood_stage": "95%"
  }
}
```

**Expected** `"acknowledged": true`.

Read back effective values (includes defaults):

**Request** — paste into Dev Tools:

```http
GET _cluster/settings?include_defaults=true&flat_settings=true
```

**Expected** dotted keys such as `cluster.routing.allocation.disk.watermark.low` under `persistent`, `transient`, and/or `defaults`.

**Fast mode**  
`bruno/Chapter 5/Lesson 1/06-watermark-settings.bru`

---

## What you learned

- How **routing awareness** and **force** zone values influence HA shard placement.
- How to read **`_cat/shards`**, **`_cluster/health`**, and **`_cluster/allocation/explain`** during incidents.
- When **force merge** helps — and when it hurts active write workloads.
- How **oversharding** and **replica** counts interact on a 3-node lab cluster.
- What **disk watermarks** do at low, high, and flood stage.

## Next lesson

[Chapter 5 Lesson 2](../Lesson%202/README.md) — mapping inspection, **shrink**, **reindex** with Painless, and versioned k-NN indexes.

## Reference scripts

| Script | Same as |
| --- | --- |
| `01-routing-awareness.py` | Step 1 |
| `02-check-shard-distribution.py` | Step 2 |
| `03-force-merge.py` | Step 3 |
| `04-index-too-many-shards.py` | Step 4 |
| `05-cluster-health-and-replicas.py` | Step 5 |
| `06-watermark-settings.py` | Step 6 |
