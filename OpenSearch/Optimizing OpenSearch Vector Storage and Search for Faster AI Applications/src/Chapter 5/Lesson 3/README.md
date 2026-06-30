# Chapter 5 · Lesson 3 — Vector storage modes

**Chapter 5 · Lesson 3** · [Voice script](../../../voice-script.docx) — k-NN **vector storage modes** and the latency vs memory trade-off.

← [Chapter 5 overview](../README.md) · [How to run labs](../../../docs/HANDS-ON-GUIDE.md)

## Overview

### Goals

By the end of this lesson you will:

1. Create **`book-embeddings-archive`** with **`mode: on_disk`** (minimal RAM, slower queries).
2. Create **`book-embeddings-efficient`** with **`mode: in_memory`** and **`data_type: float`** (lowest latency, highest memory).

### Prerequisites

- Complete [Chapter 5 · Lesson 2](../Lesson%202/README.md) (k-NN index definitions).
- Cluster with **k-NN** enabled and a version that supports the **`mode`** parameter on **`knn_vector`**.
- Open **Dev Tools** (or Bruno: [`bruno/Chapter 5/Lesson 3/`](../../../bruno/Chapter%205/Lesson%203/)).

**Save values as you go:**

| After step | Save | Used for |
| --- | --- | --- |
| Step 1 | Index **`book-embeddings-archive`** | Cold / archive tier pattern |
| Step 2 | Index **`book-embeddings-efficient`** | Hot production pattern |

---

## Lab steps

### **Step 1: Create on-disk vector index**

**Why**  
Vector indexes are often the most memory-hungry part of a RAG cluster. **`on_disk`** keeps vector values on disk and loads only graph navigation metadata into native memory — **lowest RAM footprint, slowest queries** (disk I/O bound). Use for large archives queried rarely.

**Request** — paste into Dev Tools:

```http
DELETE book-embeddings-archive
```

A `404` is fine.

```http
PUT book-embeddings-archive
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "mode": "on_disk"
      }
    }
  }
}
```

**Expected** `"acknowledged": true`.

**Fast mode**  
`bruno/Chapter 5/Lesson 3/01-book-embeddings-archive.bru`


### **Step 2: Create in-memory vector index**

**Why**  
**`in_memory`** keeps full vectors in native memory — **lowest query latency**, highest cost. Memory scales roughly as `num_docs × dimension × sizeof(data_type)`. **`data_type: float`** is the default precision; alternatives like `byte` trade accuracy for smaller footprints.

**Request** — paste into Dev Tools:

```http
DELETE book-embeddings-efficient
```

```http
PUT book-embeddings-efficient
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "mode": "in_memory",
        "data_type": "float"
      }
    }
  }
}
```

**Expected** `"acknowledged": true`.

**Fast mode**  
`bruno/Chapter 5/Lesson 3/01-book-embeddings-efficient.bru`


### **Step 3: Compare mappings (optional)**

**Why**  
Side-by-side mapping review confirms the only structural difference is `mode` (and explicit `data_type` on the hot index).

**Request** — paste into Dev Tools:

```http
GET book-embeddings-archive/_mapping
```

```http
GET book-embeddings-efficient/_mapping
```

**Expected** both indexes show `knn_vector` with `dimension: 768`; archive has `"mode": "on_disk"`, efficient has `"mode": "in_memory"` and `"data_type": "float"`.

---

## What you learned

- **`on_disk`** vs **`in_memory`** trade-off for k-NN vector storage.
- Typical tiering: **hot** working set in memory, **cold** archive on disk, often exposed via separate indexes or aliases.
- How **`data_type`** affects memory and accuracy.

## Next lesson

- **Course lesson 5-4:** secure, resilient AI apps — **mostly video**; no dedicated lab folder ([Chapter 5 overview](../README.md)).
- **Hands-on:** [Chapter 5 · Lesson 5](../Lesson%205/README.md) — priority index routing and search backpressure.

## Reference scripts

| Script | Same as |
| --- | --- |
| `01-book-embeddings-storage-modes.py` | Steps 1–2 |
