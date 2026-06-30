# Chapter 5 · Lesson 5 — Query optimization and cluster protection

**Chapter 5 · Lesson 5** · [Voice script](../../../voice-script.docx) — priority **index routing**, **search backpressure**, and node-level tuning concepts.

← [Chapter 5 overview](../README.md) · [How to run labs](../../../docs/HANDS-ON-GUIDE.md)

## Overview

### Goals

By the end of this lesson you will:

1. Pin **`orders`** and **`book-browse`** indexes to different **node tiers** with allocation `require` rules.
2. Configure **search backpressure** in **`monitor_only`** mode with thresholds and cancellation rate limits.
3. Read **search backpressure stats** per node.
4. Review **`opensearch.yml.example`** for node attributes and thread pools referenced in the course.

### Prerequisites

- Complete [Chapter 5 · Lesson 3](../Lesson%203/README.md).
- Open **Dev Tools** (or Bruno: [`bruno/Chapter 5/Lesson 5/`](../../../bruno/Chapter%205/Lesson%205/)).
- **Index routing** settings only work when nodes advertise matching attributes (for example `node.attr.node_type: power` in `opensearch.yml`). On Instaclustr managed trials you can still run the APIs; shard placement may not change until node attributes exist.
- **Search backpressure** changes cluster behavior — use your **3-node lab cluster** with instructor guidance.

---

## Lab steps

### **Step 1: Ensure demo indexes exist**

**Why**  
Routing settings apply per index. Create lightweight placeholder indexes if they are missing.

**Request** — paste into Dev Tools:

```http
PUT orders
```

```http
PUT book-browse
```

**Expected** `"acknowledged": true` for each (or index-already-exists is fine on repeat runs).

**Fast mode**  
`bruno/Chapter 5/Lesson 5/01-priority-index-routing.bru` (includes create + settings)


### **Step 2: Route `orders` to power-tier nodes**

**Why**  
In a tiered cluster, **`index.routing.allocation.require.<attr>`** forces *all* shards for an index onto nodes where that attribute matches — keeping latency-sensitive data on fast hardware.

Related options: **`include`** (any match), **`exclude`** (none match).

**Request** — paste into Dev Tools:

```http
PUT orders/_settings
{
  "index.routing.allocation.require.node_type": "power"
}
```

**Expected** `"acknowledged": true`.

**Prerequisite:** nodes must set `node.attr.node_type: power` (see **`opensearch.yml.example`** in this folder).


### **Step 3: Route `book-browse` to standard-tier nodes**

**Why**  
Large, bursty browse workloads can live on cheaper **standard** nodes without competing with **`orders`** for CPU and heap.

**Request** — paste into Dev Tools:

```http
PUT book-browse/_settings
{
  "index.routing.allocation.require.node_type": "standard"
}
```

**Expected** `"acknowledged": true`.

Verify shard placement when node attributes are configured:

**Request** — paste into Dev Tools:

```http
GET _cat/shards/orders,book-browse?v&h=index,shard,prirep,node
```

**Expected** shards on nodes whose `node_type` matches each index's require rule.

**Fast mode**  
Steps 2–3 in `bruno/Chapter 5/Lesson 5/01-priority-index-routing.bru`


### **Step 4: Apply search backpressure thresholds**

**Why**  
**Search backpressure** cancels expensive in-flight searches when a node is under stress — trading individual query completion for cluster stability. Start in **`monitor_only`** to see what *would* be cancelled before switching to **`enforced`**.

**Request** — paste into Dev Tools:

```http
PUT _cluster/settings
{
  "persistent": {
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

**Threshold summary:**

| Setting | Meaning |
| --- | --- |
| `cpu_time_millis_threshold: 30000` | Per-shard task using > 30s CPU is "expensive" |
| `elapsed_time_millis_threshold: 45000` | Per-shard task running > 45s wall-clock is "expensive" |
| `total_heap_percent_threshold: 0.05` | Coordinator buffering > 5% of JVM heap is "expensive" |
| `node_duress.cpu_threshold: 0.90` | Backpressure activates only when node CPU is stressed |
| `node_duress.heap_threshold: 0.70` | …and heap usage is high |


### **Step 5: Apply cancellation rate limits**

**Why**  
Rate limits prevent a burst of cancellations from causing its own outage. **`cancellation_rate`** caps how many tasks can be cancelled per second; **`cancellation_burst`** allows short spikes.

**Request** — paste into Dev Tools:

```http
PUT _cluster/settings
{
  "persistent": {
    "search_backpressure.search_task.cancellation_rate": 0.05,
    "search_backpressure.search_task.cancellation_burst": 10,
    "search_backpressure.search_shard_task.cancellation_rate": 0.05,
    "search_backpressure.search_shard_task.cancellation_burst": 15
  }
}
```

**Expected** `"acknowledged": true`.

**Fast mode**  
`bruno/Chapter 5/Lesson 5/02-search-backpressure.bru`


### **Step 6: Read backpressure stats**

**Why**  
Confirms **`monitor_only`** is observing traffic and shows per-node counters before you enable **`enforced`**.

**Request** — paste into Dev Tools:

```http
GET _nodes/stats/search_backpressure
```

**Expected** JSON with per-node `search_backpressure` stats (mode, resource trackers, cancellation counts).


### **Step 7: Review node config reference (optional)**

**Why**  
Index routing (Steps 2–3) and [Lesson 1](../Lesson%201/README.md) zone awareness require matching **`node.attr.*`** in node configuration. The course also discusses thread pools and cluster manager bootstrap.

Open **`opensearch.yml.example`** in this folder. It includes:

- **`thread_pool.search`** and **`thread_pool.write`** sizing
- **`cluster.initial_cluster_manager_nodes`** for a 3-node cluster

**Do not** paste production secrets or restart managed Instaclustr nodes without provider guidance — use the file as a **reference** aligned with the video lesson.

---

## What you learned

- How **`allocation.require`** pins indexes to hardware tiers.
- How **search backpressure** thresholds, **node duress**, and **cancellation rate limits** protect overloaded nodes.
- Where **node attributes** and **thread pools** fit in the course narrative.

## Course wrap-up

You have completed the hands-on path for **Chapter 5**. Lesson **5-4** (secure, resilient AI apps) is covered primarily in **video** — see [Chapter 5 README](../README.md).

## Reference scripts

| Script | Same as |
| --- | --- |
| `01-priority-index-routing.py` | Steps 1–3 |
| `02-search-backpressure.py` | Steps 4–6 |
