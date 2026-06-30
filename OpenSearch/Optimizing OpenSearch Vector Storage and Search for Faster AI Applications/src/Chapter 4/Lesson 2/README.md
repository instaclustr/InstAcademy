# Chapter 4 Lesson 2 — Optimizing indexes for RAG pipelines

**InstAcademy → OpenSearch:** Lesson **4-2** · [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications](../../../OpenSearch%20Learning%20Path%201.docx) — fix common index mistakes (wrong field types, missing vectors), add chunking, tune bulk load throughput, size shards, and preload vector files.

## Overview

### Goals

By the end of this lesson you will:

1. Create a deliberately **unoptimized** baseline index **`books-unoptimized`**
2. Build **`bookstore-chunking-pipeline`** (chunk + Painless normalize + embed)
3. Create production-shaped **`bookstore-rag`** (FAISS k-NN, nested chunks, slower refresh)
4. **Bulk load** with refresh disabled, **force merge**, restore refresh
5. Inspect shard sizes with **`_cat/shards`**
6. **Warm** k-NN and set **`index.store.preload`** for vector files

### Prerequisites

- Complete [Chapter 4 Lesson 1](../Lesson%201/README.md) — **`ML_MODEL_ID`** in **`src/.env`**
- Open **Dev Tools** (or Bruno: [`bruno/Chapter 4/Lesson 2/`](../../../bruno/Chapter%204/Lesson%202/))

---

## Lab steps

### **Step 1: Create the unoptimized baseline index**

**Why**  
This index has intentional problems — **`text`** on ISBN/genre (breaks exact filters), no vectors, default refresh — so later steps show clear before/after wins.

Skip if **`books-unoptimized`** already exists.

**Request** — paste into Dev Tools:

```http
PUT books-unoptimized
{
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  },
  "mappings": {
    "properties": {
      "book_id": { "type": "text" },
      "title": { "type": "text" },
      "author": { "type": "text" },
      "isbn": { "type": "text" },
      "genre": { "type": "text" },
      "published_year": { "type": "integer" },
      "price": { "type": "float" },
      "rating": { "type": "integer" },
      "content": { "type": "text" }
    }
  }
}
```

**Fast mode**  
`bruno/Chapter 4/Lesson 2/01-create-books-unoptimized.bru`


### **Step 2: Create the chunking ingest pipeline**

**Why**  
Sentence transformers truncate long text. Chunking preserves RAG snippets; embedding the full **`content`** still gives a whole-document k-NN vector.

Replace `YOUR_MODEL_ID`:

**Request** — paste into Dev Tools:

```http
PUT _ingest/pipeline/bookstore-chunking-pipeline
{
  "description": "Chunk book content for RAG embedding",
  "processors": [
    {
      "text_chunking": {
        "algorithm": {
          "fixed_token_length": {
            "token_limit": 384,
            "overlap_rate": 0.2,
            "tokenizer": "standard"
          }
        },
        "field_map": {
          "content": "content_chunks"
        }
      }
    },
    {
      "script": {
        "lang": "painless",
        "source": "if (ctx.content_chunks == null) { ctx.content_chunks = []; } else { def normalized_chunks = []; for (int i = 0; i < ctx.content_chunks.size(); i++) { def chunk = ctx.content_chunks.get(i); if (chunk != null) { normalized_chunks.add(['text': chunk, 'chunk_index': i]); } } ctx.content_chunks = normalized_chunks; }"
      }
    },
    {
      "text_embedding": {
        "model_id": "YOUR_MODEL_ID",
        "field_map": {
          "content": "content_embedding"
        }
      }
    }
  ]
}
```

**Fast mode**  
`02-create-chunking-pipeline.bru`


### **Step 3: Create the optimized bookstore-rag index**

**Why**  
FAISS HNSW, **`refresh_interval: 30s`**, **`keyword`** genre, nested **`content_chunks`**.

Delete if re-running:

**Request** — paste into Dev Tools:

```http
DELETE bookstore-rag
```

Create:

```http
PUT bookstore-rag
{
  "settings": {
    "index": {
      "knn": true,
      "default_pipeline": "bookstore-chunking-pipeline",
      "refresh_interval": "30s"
    }
  },
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "author": { "type": "text" },
      "content": { "type": "text" },
      "content_chunks": {
        "type": "nested",
        "properties": {
          "text": { "type": "text" },
          "chunk_index": { "type": "integer" }
        }
      },
      "content_embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "engine": "faiss",
          "name": "hnsw",
          "parameters": {
            "m": 16,
            "ef_construction": 128
          }
        }
      },
      "genre": { "type": "keyword" },
      "price": { "type": "float" },
      "rating": { "type": "float" },
      "publication_year": { "type": "integer" },
      "in_stock": { "type": "boolean" }
    }
  }
}
```

**Fast mode**  
`03-delete-bookstore-rag.bru` (optional) → `04-create-bookstore-rag.bru`


### **Step 4: Optimized bulk load**

**Why each phase:** disable refresh during load → bulk → force merge → restore refresh → explicit refresh.

### 4a — Disable refresh

**Request** — paste into Dev Tools:


```http
PUT bookstore-rag/_settings
{
  "index": {
    "refresh_interval": "-1"
  }
}
```

### 4b — Bulk index

**Inline smoke test (1 book):**

**Request** — paste into Dev Tools:


```http
POST _bulk
{ "index": { "_index": "bookstore-rag", "_id": "2701" } }
{ "id": "2701", "title": "Moby Dick; Or, The Whale", "content": "\"Moby Dick; Or, The Whale\" by Herman Melville is an epic novel published in 1851. Sailor Ishmael narrates the obsessive quest of Captain Ahab, who commands the whaling ship Pequod in pursuit of Moby Dick, a giant white sperm whale that destroyed his leg. Ahab's monomaniacal hunt for vengeance drives the ship and its diverse crew across the world's oceans, blending realistic whaling details with profound explorations of good, evil, fate, and human nature in this cornerstone of American literature. (This is an automatically generated summary.)" }
```

**Full dataset:** use [`rest/bulk/chapter-4-bookstore-rag-index.ndjson`](../../../rest/bulk/chapter-4-bookstore-rag-index.ndjson) but change **`_index`** to **`bookstore-rag`** and map **`passage_text`** → **`content`** if you adapt the file (or bulk from Python — see optional scripts).

Allow several minutes for chunking + embedding.

### 4c — Force merge

**Request** — paste into Dev Tools:


```http
POST bookstore-rag/_forcemerge?max_num_segments=5
```

### 4d — Restore refresh and make docs visible

**Request** — paste into Dev Tools:


```http
PUT bookstore-rag/_settings
{
  "index": {
    "refresh_interval": "1s"
  }
}
```

**Request** — paste into Dev Tools:


```http
POST bookstore-rag/_refresh
```

**Fast mode**  
`05-disable-refresh.bru` → `06-bulk-bookstore-rag.bru` → `07-force-merge.bru` → `08-restore-refresh.bru` → `09-refresh-index.bru`


### **Step 5: Inspect shard sizes**

**Why**  
Shard count is hard to change later; target ~10–50 GB per shard depending on workload.

**Request** — paste into Dev Tools:

```http
GET _cat/shards/bookstore-rag?v&h=index,shard,prirep,state,docs,store&format=json
```

**Rules of thumb:**

```
number_of_shards = total_data_size_GB / target_shard_size_GB
```

- Search-heavy RAG: **10–30 GB** per shard  
- Write-heavy: **30–50 GB** per shard  
- Latency-sensitive vector/hybrid: start **50 GB**, reduce toward **10 GB** if needed

**Fast mode**  
`10-cat-shards.bru`


### **Step 6: Warm k-NN and preload vector files**

**Why**  
Warmup loads HNSW graphs into native memory; **`index.store.preload`** mmap's **`vec`** / **`vem`** files on index open (requires close → settings → open).

**Request** — paste into Dev Tools:

```http
GET _plugins/_knn/warmup/bookstore-rag
```

```http
GET _plugins/_knn/stats
```

Close, set preload, reopen:

```http
POST bookstore-rag/_close
```

```http
PUT bookstore-rag/_settings
{
  "index": {
    "store": {
      "preload": ["vec", "vem"]
    }
  }
}
```

**Request** — paste into Dev Tools:


```http
POST bookstore-rag/_open
```

Wait for yellow/green:

**Request** — paste into Dev Tools:


```http
GET _cluster/health/bookstore-rag?wait_for_status=yellow&timeout=60s
```

**Fast mode**  
`11-knn-warmup.bru` → `12-close-index.bru` → `13-set-preload.bru` → `14-open-index.bru`

---

## What you learned

- Mapping choices that matter for RAG (**keyword** vs **text**, **nested** chunks, FAISS k-NN)
- The canonical **fast bulk** recipe (refresh off → merge → refresh on)
- How to read **shard size** and **warm** vector indexes

## Next lesson

[Chapter 4 Lesson 3](../Lesson%203/README.md) — **explain**, **`_rank_eval`**, and search pipelines with business filters.

## Reference scripts

| Script | Same as |
|--------|---------|
| `00-set-up-books-unoptimized.py` | Step 1 |
| `01-chunking-pipeline.py` | Step 2 |
| `02-bookstore-rag.py` | Step 3 |
| `03-bulk-loading-optimized.py` | Step 4 (full bulk from `src/sample-data.json`) |
| `04-shard-sizing.py` | Step 5 |
| `05-warming-and-preload.py` | Step 6 |
| `06-put-it-all-together.py` | End-to-end on parallel index **`bookstore-rag-all-together`** |

```bash
python 00-set-up-books-unoptimized.py
python 01-chunking-pipeline.py
python 02-bookstore-rag.py
python 03-bulk-loading-optimized.py
python 04-shard-sizing.py
python 05-warming-and-preload.py
```

Run **`06-put-it-all-together.py`** separately for a consolidated demo index.
