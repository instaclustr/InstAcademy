# Chapter 5 · Lesson 2 — Index optimization

**Chapter 5 · Lesson 2** · [Voice script](../../../voice-script.docx) — mappings, shrink, reindex with Painless, and versioned k-NN index definitions.

← [Chapter 5 overview](../README.md) · [How to run labs](../../../docs/HANDS-ON-GUIDE.md)

## Overview

### Goals

By the end of this lesson you will:

1. Create and inspect a **bookstore mapping** on **`my-index`**.
2. Run the canonical **shrink** workflow on **`bookstore-rag-all-together`** with an alias swap.
3. **Reindex** with a **Painless** script that transforms documents.
4. Create **versioned k-NN indexes** (`book-embeddings-v2`, `book-embeddings-v3`) with different dimensions and HNSW parameters.

### Prerequisites

- Complete [Chapter 5 · Lesson 1](../Lesson%201/README.md) (shard basics).
- Ensure **`bookstore-rag-all-together`** exists ([Chapter 4 · Lesson 2](../../Chapter%204/Lesson%202/README.md) script **`06`**).
- Open **Dev Tools** (or Bruno: [`bruno/Chapter 5/Lesson 2/`](../../../bruno/Chapter%205/Lesson%202/)).

**Save values as you go:**

| After step | Save | Used for |
| --- | --- | --- |
| Step 1 | Index **`my-index`** | Steps 2–4 |
| Step 2 | A **node name** from `_cat/nodes` | Step 3 shrink pin |
| Step 3 | Alias **`bookstore-rag-all-together-alias`** | Client queries after shrink |

---

## Lab steps

### **Step 1: Create `my-index` with bookstore mappings**

**Why**  
Mappings are mostly immutable. This recreates a known single-shard index for mapping inspection and reindex demos. Field types mirror the Chapter 1 keyword bookstore example.

**Request** — paste into Dev Tools:

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
        "fields": {
          "keyword": { "type": "keyword", "ignore_above": 256 }
        }
      },
      "author": { "type": "keyword" },
      "isbn": { "type": "keyword" },
      "genre": { "type": "keyword" },
      "publisher": { "type": "keyword" },
      "description": { "type": "text" },
      "price": { "type": "float" },
      "in_stock": { "type": "boolean" },
      "published_year": { "type": "integer" }
    }
  }
}
```

**Expected** `"acknowledged": true`.

**Fast mode**  
`bruno/Chapter 5/Lesson 2/00-create-my-index-bookstore.bru`


### **Step 2: Read the mapping**

**Why**  
`GET /<index>/_mapping` is the first call when debugging analysis, field types, or comparing staging vs production schemas. The inner `mappings` block is the shape you'd pass to `indices.create`.

**Request** — paste into Dev Tools:

```http
GET my-index/_mapping
```

**Expected** JSON keyed by index name, containing `mappings.properties` with `title`, `author`, `isbn`, etc.

**Fast mode**  
`bruno/Chapter 5/Lesson 2/01-get-mapping.bru`


### **Step 3: Shrink `bookstore-rag-all-together`**

**Why**  
**Shrink** recreates an index with **fewer primary shards** (target count must divide the source primary count). Use it when an index is read-only and over-sharded — common after time-series roll-off or post-bulk-load optimization.

**Six-step recipe** (memorize this pattern):

1. Pin all shards to one node and block writes.
2. Call `_shrink` to the target index.
3. Remove the pin so the new index can rebalance.
4. Force-merge to one segment (read-only index).
5. Atomically swap an alias.
6. Delete the source index.

### 3a — Find a node name

On Instaclustr, node names differ from `node-1`. List them:

**Request** — paste into Dev Tools:

```http
GET _cat/nodes?v&h=name
```

**Save**  
one node name (for example the first data node). Replace **`YOUR_NODE_NAME`** in the requests below.

### 3b — Create the alias (if missing)

The shrink script swaps **`bookstore-rag-all-together-alias`**. Create it on the source index if it does not exist yet:

**Request** — paste into Dev Tools:

```http
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "bookstore-rag-all-together",
        "alias": "bookstore-rag-all-together-alias"
      }
    }
  ]
}
```

**Expected** `"acknowledged": true`.

### 3c — Pin shards and block writes

**Request** — paste into Dev Tools:

```http
PUT bookstore-rag-all-together/_settings
{
  "settings": {
    "index.routing.allocation.require._name": "YOUR_NODE_NAME",
    "index.blocks.write": true
  }
}
```

**Expected** `"acknowledged": true`. Wait until `_cat/shards` shows all primaries on that node.

### 3d — Shrink to the target index

**Request** — paste into Dev Tools:

```http
POST bookstore-rag-all-together/_shrink/bookstore-rag-all-together-shrunk
{
  "settings": {
    "index.number_of_shards": 1,
    "index.number_of_replicas": 1,
    "index.codec": "best_compression"
  }
}
```

**Expected** `"acknowledged": true`. The target index appears when the task completes.

### 3e — Remove routing requirement

**Request** — paste into Dev Tools:

```http
PUT bookstore-rag-all-together-shrunk/_settings
{
  "index.routing.allocation.require._name": null
}
```

**Expected** `"acknowledged": true`.

### 3f — Force-merge shrunk index

**Request** — paste into Dev Tools:

```http
POST bookstore-rag-all-together-shrunk/_forcemerge?max_num_segments=1
```

**Expected**  
merge task completes; one segment per shard is ideal for static read-only data.

### 3g — Atomic alias swap

**Request** — paste into Dev Tools:

```http
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "bookstore-rag-all-together",
        "alias": "bookstore-rag-all-together-alias"
      }
    },
    {
      "add": {
        "index": "bookstore-rag-all-together-shrunk",
        "alias": "bookstore-rag-all-together-alias"
      }
    }
  ]
}
```

**Expected** `"acknowledged": true`. Clients querying the alias now hit the shrunk index.

### 3h — Delete the source index

**Request** — paste into Dev Tools:

```http
DELETE bookstore-rag-all-together
```

**Expected** `"acknowledged": true`.

Verify shard counts:

**Request** — paste into Dev Tools:

```http
GET _cat/shards/bookstore-rag-all-together-shrunk?v
```

**Expected**  
fewer shard rows than the original multi-shard index.

**Fast mode**  
`bruno/Chapter 5/Lesson 2/02-shrink-index.bru`


### **Step 4: Bulk sample docs into `my-index` (for reindex demo)**

**Why**  
Reindex with a transform is easier to verify when source documents exist.

**Request** — paste into Dev Tools:

```http
POST _bulk
{ "index": { "_index": "my-index", "_id": "978-0143127740" } }
{ "book_id": "978-0143127740", "isbn": "978-0143127740", "title": "The Martian", "author": "Andy Weir", "genre": "Science Fiction", "publisher": "Crown Publishing", "description": "An astronaut stranded on Mars fights to survive.", "price": 16.99, "in_stock": true, "published_year": 2014 }
{ "index": { "_index": "my-index", "_id": "978-0307277677" } }
{ "book_id": "978-0307277677", "isbn": "978-0307277677", "title": "The Road", "author": "Cormac McCarthy", "genre": "Fiction", "publisher": "Vintage", "description": "A father and son journey through a post-apocalyptic landscape.", "price": 15.95, "in_stock": true, "published_year": 2006 }
```

**Expected** `"errors": false` in the bulk response.

**Request** — paste into Dev Tools:

```http
POST my-index/_refresh
```


### **Step 5: Reindex with Painless transformation**

**Why**  
`_reindex` server-side copies documents from one index to another. Use it when mappings are incompatible, shard counts must change, or every document needs a transform. The demo merges `author` into `title` and drops `author` — the pattern (`ctx._source` mutations, `ctx.op = 'noop'`) applies to real migrations.

Create the destination index (same mapping is fine for this demo):

**Request** — paste into Dev Tools:

```http
PUT my-index-new
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
      "title": { "type": "text" },
      "isbn": { "type": "keyword" },
      "genre": { "type": "keyword" },
      "publisher": { "type": "keyword" },
      "description": { "type": "text" },
      "price": { "type": "float" },
      "in_stock": { "type": "boolean" },
      "published_year": { "type": "integer" }
    }
  }
}
```

Run reindex with **`slices=5`** (parallel sub-tasks) and wait for completion:

**Request** — paste into Dev Tools:


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

**Expected** `"total"`, `"created"`, and `"failures": []` in the response.

Verify a document:

**Request** — paste into Dev Tools:

```http
GET my-index-new/_search
{
  "size": 1
}
```

**Expected** `title` contains the author name; no `author` field in `_source`.

**Fast mode**  
`bruno/Chapter 5/Lesson 2/03-reindex-books.bru`


### **Step 6: Create `book-embeddings-v2`**

**Why**  
Embedding models change dimensions and similarity behavior. **Versioned index names** (`v2`, `v3`) let you backfill a new index and swap an alias without downtime. Store **`model_version`** per document so you can audit recall regressions.

**Request** — paste into Dev Tools:

```http
DELETE book-embeddings-v2
```

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
          "parameters": {
            "ef_construction": 128,
            "m": 16
          }
        }
      },
      "model_version": { "type": "keyword" },
      "created_at": { "type": "date" }
    }
  }
}
```

**Expected** `"acknowledged": true`.

**Fast mode**  
`bruno/Chapter 5/Lesson 2/04-create-book-embeddings-v2.bru`


### **Step 7: Create `book-embeddings-v3` (higher recall settings)**

**Why**  
When evaluation shows v2 recall is too low, you might switch to a **1024-dim** model and **denser HNSW** graph (`ef_construction: 256`, `m: 32`) — slower indexing, more memory, better recall.

**Request** — paste into Dev Tools:

```http
DELETE book-embeddings-v3
```

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
          "parameters": {
            "ef_construction": 256,
            "m": 32
          }
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

**Fast mode**  
`bruno/Chapter 5/Lesson 2/05-create-book-embeddings-v3.bru`

---

## What you learned

- How to read and reason about **index mappings**.
- The canonical **shrink + alias swap** workflow for reducing shard count on read-only indexes.
- How **`_reindex`** with **Painless** transforms documents at scale (`slices` for parallelism).
- Why **versioned k-NN indexes** and per-doc **model metadata** matter when models change.

## Next lesson

[Chapter 5 · Lesson 3](../Lesson%203/README.md) — **vector storage modes** (`on_disk` vs `in_memory`).

## Reference scripts

| Script | Same as |
| --- | --- |
| `00-create-my-index-bookstore.py` | Step 1 |
| `01-get-mapping.py` | Step 2 |
| `02-shrink-index.py` | Step 3 (uses hard-coded `node-1`; replace with your node name in Dev Tools) |
| `03-reindex-books.py` | Step 5 |
| `04-create-book-embeddings-v2.py` | Step 6 |
| `05-create-book-embeddings-v3.py` | Step 7 |
