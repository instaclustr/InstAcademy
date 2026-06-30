# Chapter 1 Lesson 4 — Vector storage and search optimizations

**InstAcademy → OpenSearch:** Lesson 1-4 · [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications](../../OpenSearch%20Learning%20Path%201.docx) — `knn_vector` indexes, HNSW, and reducing dimensions with `_reindex`.

## Overview

### Goals

1. Create a **256-dimensional** `knn_vector` index and index three sample documents.
2. Create a **128-dimensional** destination index.
3. Use **`_reindex`** with **Painless** to truncate vectors — a pattern for memory/storage optimization.

### Prerequisites

- Complete [Lesson 1-1](../1-1/README.md) (cluster connectivity).
- Open **Dev Tools**.

---

## Lab steps

### **Step 1: Delete previous run (optional)**

**Request** — paste into Dev Tools:


```http
DELETE my-optimized-vector-index
```

**Request** — paste into Dev Tools:


```http
DELETE my-vector-index
```

404 responses are fine.

**Fast mode**  
`bruno/Chapter 1/Lesson 1-4/01-delete-indexes.bru`


### **Step 2: Create source index (256-dim vectors)**

**Why**  
`knn_vector` requires `index.knn: true`. HNSW (`method.name: hnsw`) is the approximate nearest-neighbor graph OpenSearch uses for vector search. The **`dimension`** must match stored vectors exactly.

**Request** — paste into Dev Tools:

```http
PUT my-vector-index
{
  "settings": { "index.knn": true },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "my_vector": {
        "type": "knn_vector",
        "dimension": 256,
        "method": {
          "engine": "lucene",
          "space_type": "l2",
          "name": "hnsw",
          "parameters": {}
        }
      }
    }
  }
}
```

**Expected** `"acknowledged": true`


### **Step 3: Bulk three sample documents**

**Why**  
Vectors are large — use the pre-generated bulk file rather than typing 256 floats per document.

**Option A — Dev Tools:** paste the contents of [`rest/bulk/chapter-1-lesson-4-vector-index.ndjson`](../../rest/bulk/chapter-1-lesson-4-vector-index.ndjson) after:

**Request** — paste into Dev Tools:

```http
POST _bulk
```

**Option B — generate the file** (maintainers / after clone):

```bash
python tools/generate-bulk-ndjson.py
```

**Expected** `"errors": false`, three successful index actions.

**Request** — paste into Dev Tools:

```http
POST my-vector-index/_refresh
```

**Fast mode**  
`bruno/Chapter 1/Lesson 1-4/03-bulk-sample-vectors.bru`


### **Step 4: Create destination index (128-dim)**

**Request** — paste into Dev Tools:


```http
PUT my-optimized-vector-index
{
  "settings": { "index.knn": true },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "my_vector": {
        "type": "knn_vector",
        "dimension": 128,
        "method": {
          "engine": "lucene",
          "space_type": "l2",
          "name": "hnsw",
          "parameters": {}
        }
      }
    }
  }
}
```


### **Step 5: Reindex with Painless truncation**

**Why**  
Halving dimensions roughly halves HNSW graph memory. `_reindex` transforms each document server-side before writing to the destination index.

**Request** — paste into Dev Tools:

```http
POST _reindex?wait_for_completion=true
{
  "source": { "index": "my-vector-index" },
  "dest": { "index": "my-optimized-vector-index" },
  "script": {
    "source": "ctx._source.my_vector = ctx._source.my_vector.subList(0, 128);",
    "lang": "painless"
  }
}
```

**Expected**

```json
{
  "took": ...,
  "timed_out": false,
  "total": 3,
  "updated": 0,
  "created": 3,
  "deleted": 0,
  "failures": []
}
```

Confirm hits exist:

**Request** — paste into Dev Tools:

```http
GET my-optimized-vector-index/_search
{
  "size": 3,
  "_source": ["title"]
}
```

**Fast mode**  
`bruno/Chapter 1/Lesson 1-4/05-reindex-truncate.bru`

---

## What you learned

- How **`knn_vector`** mappings and **`index.knn`** work together.
- Using **`_reindex`** + **Painless** to shrink vectors in flight.

## Next chapter

[Chapter 2](../../Chapter%202/README.md) — register a real embedding model and build a neural search pipeline.

## Reference scripts

| Script | Same as |
|--------|---------|
| `main.py` | Steps 2–5 with deterministic sample vectors |
