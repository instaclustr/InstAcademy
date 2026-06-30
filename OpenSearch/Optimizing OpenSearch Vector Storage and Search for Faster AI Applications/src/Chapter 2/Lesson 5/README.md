# Chapter 2 Lesson 5 — Optimizing neural search (cluster routing)

**InstAcademy → OpenSearch:** Lesson 2-5 · [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications](../../../OpenSearch%20Learning%20Path%201.docx) — cluster-level **routing** settings that control shard allocation and rebalancing during maintenance and at scale.

## Overview

### Goals

By the end of this lesson you will:

1. Set **`cluster.routing.allocation.enable`** to **`all`** (allow shard allocation).
2. Set **`cluster.routing.rebalance.enable`** to **`all`** (allow shard rebalancing).
3. Understand when operators temporarily restrict these settings during rolling restarts or node maintenance.

This lesson is **standalone operations practice** — it does not require Lesson 2 indexes or ML models.

### Prerequisites

- Complete [Chapter 1 Lesson 1-1](../../Chapter%201/1-1/README.md) (cluster connectivity).
- Open **Dev Tools** on a **lab cluster** only — routing changes affect **every index** on the cluster (or Bruno fast mode: [`bruno/Chapter 2/Lesson 5/`](../../../bruno/Chapter%202/Lesson%205/)).

| Setting | Lab value | Meaning |
|---------|-----------|---------|
| `cluster.routing.allocation.enable` | `all` | Cluster may allocate shards to nodes |
| `cluster.routing.rebalance.enable` | `all` | Cluster may move shards to balance load |

Allowed values (reference):

- **`allocation.enable`:** `all` \| `primaries` \| `new_primaries` \| `none`
- **`rebalance.enable`:** `all` \| `primaries` \| `replicas` \| `none`

During maintenance, operators often set **`allocation.enable`** to **`none`** before a rolling restart, then restore **`all`** when nodes are healthy.

---

## Lab steps

### **Step 1: Verify cluster connectivity**

**Why**  
Cluster settings require a healthy connection to the elected master node.

**Request** — paste into Dev Tools:

```http
GET /
```

**Expected**

```json
{
  "name": "...",
  "cluster_name": "...",
  "cluster_uuid": "...",
  "version": { "number": "2.x.x" },
  "tagline": "The OpenSearch Project: https://opensearch.org/"
}
```

**Fast mode**  
`bruno/Chapter 2/Lesson 5/01-cluster-info.bru`


### **Step 2: Set persistent routing settings**

**Why**  
**`persistent`** settings survive a full cluster restart (unlike **`transient`**). For day-to-day operation both routing knobs should be **`all`** so new shards allocate and the cluster can rebalance after node changes.

Neural search workloads are memory- and CPU-intensive; balanced shard placement helps avoid hot nodes. These settings do not tune k-NN directly — they control **where** shards live, not **how** vectors are indexed.

**Request** — paste into Dev Tools:

```http
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": "all",
    "cluster.routing.rebalance.enable": "all"
  }
}
```

**Expected**

```json
{
  "acknowledged": true,
  "persistent": {
    "cluster.routing.allocation.enable": "all",
    "cluster.routing.rebalance.enable": "all"
  }
}
```

**Save**  
no ids — note the settings you applied. After maintenance, confirm both are back to **`all`** or new shards may remain unassigned.

Optional (commented out in the course Python script): **`cluster.routing.allocation.allow_rebalance`** — set to **`indices_all_active`** if you want rebalancing only after all index shards are active.

**Fast mode**  
`bruno/Chapter 2/Lesson 5/02-cluster-routing-settings.bru`


### **Step 3: Confirm current cluster settings (optional)**

**Why**  
Verify the master accepted your persistent routing configuration.

**Request** — paste into Dev Tools:

```http
GET _cluster/settings?include_defaults=false&flat_settings=true
```

**Expected** Response includes your **`persistent`** routing keys with value **`all`**.

**Fast mode**  
`bruno/Chapter 2/Lesson 5/03-get-cluster-settings.bru`

---

## What you learned

- What **`cluster.routing.allocation.enable`** and **`cluster.routing.rebalance.enable`** control.
- Why **`persistent`** scope is appropriate for operational routing defaults.
- When to restrict allocation/rebalance during **maintenance** on production clusters.

## Next lesson

Continue to [Chapter 3](../../Chapter%203/README.md) — **neural sparse encoding**, sparse ingest pipelines, and hybrid search with score normalization.

## Reference scripts

| Script | Same as |
|--------|---------|
| `001-cluster-routing-settings.py` | Step 2 (PUT persistent routing settings) |
