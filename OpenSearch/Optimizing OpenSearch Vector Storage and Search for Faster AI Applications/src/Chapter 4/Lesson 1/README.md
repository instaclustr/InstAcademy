# Chapter 4 · Lesson 1 — Optimizing RAG pipelines in OpenSearch

**Chapter 4 · Lesson 1** · [Voice script](../../../voice-script.docx) — RAG performance and accuracy levers: stronger embeddings, ingest pipelines, k-NN retrieval, hybrid normalization, and k-NN cache warmup.

← [Chapter 4 overview](../README.md) · [How to run labs](../../../docs/HANDS-ON-GUIDE.md)

## Overview

### Goals

By the end of this lesson you will:

1. Register and deploy **`huggingface/sentence-transformers/all-mpnet-base-v2`** (768-dim dense embeddings)
2. Create **`bookstore-rag-ingest-pipeline`** and **`bookstore-rag-index`**
3. Bulk-load books from **`src/sample-data.json`**
4. Run pure **k-NN** search with a stored query vector
5. Create **`bookstore-hybrid-pipeline`** and run **hybrid** (BM25 + k-NN) search
6. Warm k-NN graphs and inspect the memory circuit breaker

**Why a stronger model?** Chapter 2 used DistilBERT (fast baseline). RAG retrieval quality depends heavily on embedding quality; **`all-mpnet-base-v2`** trades speed for higher recall on general English.

### Prerequisites

- Complete [Chapter 1 · Lesson 1](../../Chapter%201/Lesson%201/README.md).
- Open **Dev Tools** (or Bruno: [`bruno/Chapter 4/Lesson 1/`](../../../bruno/Chapter%204/Lesson%201/)).
- Save **`model_group_id`**, **`model_id`**, **`task_id`**; set **`ML_MODEL_ID`** in **`src/.env`** after deploy.
- For k-NN / hybrid steps, open **`001-bookstore-rag-query-vector.json`** in this folder — a pre-baked 768-dimensional query vector used by the lab scripts (paste its array into the `"vector"` field below).

---

## Lab steps

### **Step 1: Enable URL model registration**

**Request** — paste into Dev Tools:


```http
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.allow_registering_model_via_url": true
  }
}
```

**Fast mode**  
`bruno/Chapter 4/Lesson 1/02-enable-url-model-registration.bru`


### **Step 2: Register model group (skip if exists)**

Reuse **`huggingface-models`** from earlier chapters if present; otherwise:

**Request** — paste into Dev Tools:


```http
POST _plugins/_ml/model_groups/_register
{
  "name": "huggingface-models",
  "description": "A group for Hugging Face transformer models"
}
```

**Save:** **`model_group_id`**

**Fast mode**  
`03-register-model-group.bru`


### **Step 3: Register all-mpnet-base-v2**

Replace `YOUR_MODEL_GROUP_ID`:

**Request** — paste into Dev Tools:


```http
POST _plugins/_ml/models/_register
{
  "name": "huggingface/sentence-transformers/all-mpnet-base-v2",
  "version": "1.0.1",
  "model_group_id": "YOUR_MODEL_GROUP_ID",
  "model_format": "TORCH_SCRIPT"
}
```

#### **Poll registration**

**Request** — paste into Dev Tools:


```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

Wait for **`"state": "COMPLETED"`**. **Save `model_id`.**

**Fast mode**  
`04-register-mpnet-model.bru` → `05-poll-ml-task.bru`


### **Step 4: Deploy the model**

**Request** — paste into Dev Tools:


```http
POST _plugins/_ml/models/YOUR_MODEL_ID/_deploy
```

Poll if deploy returns **`task_id`**. Add **`ML_MODEL_ID=YOUR_MODEL_ID`** to **`src/.env`**.

**Fast mode**  
`06-deploy-model.bru` → `07-poll-ml-task-deploy.bru`


### **Step 5: Create the RAG ingest pipeline**

**Why**  
Auto-embed **`passage_text`** → **`passage_embedding`** on every indexed document.

Replace `YOUR_MODEL_ID`:

**Request** — paste into Dev Tools:

```http
PUT _ingest/pipeline/bookstore-rag-ingest-pipeline
{
  "description": "Pipeline for processing OpenSearch index data",
  "processors": [
    {
      "text_embedding": {
        "model_id": "YOUR_MODEL_ID",
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```

**Fast mode**  
`08-create-rag-ingest-pipeline.bru`


### **Step 6: Create bookstore-rag-index**

**Why**  
**`index.knn: true`** enables HNSW queries; **`default_pipeline`** wires automatic embedding; 768 dimensions match the model output.

Skip delete if the index already exists and you want to preserve data.

**Request** — paste into Dev Tools:

```http
PUT bookstore-rag-index
{
  "settings": {
    "index.knn": true,
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    },
    "default_pipeline": "bookstore-rag-ingest-pipeline"
  },
  "mappings": {
    "properties": {
      "book_id": { "type": "keyword" },
      "title": { "type": "text" },
      "author": { "type": "text" },
      "isbn": { "type": "keyword" },
      "genre": { "type": "keyword" },
      "published_year": { "type": "integer" },
      "chunk_index": { "type": "integer" },
      "passage_text": { "type": "text" },
      "passage_embedding": {
        "type": "knn_vector",
        "dimension": 768,
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

**Fast mode**  
`09-create-bookstore-rag-index.bru`


### **Step 7: Bulk index books**

**Option A — inline (2 books):**

**Request** — paste into Dev Tools:


```http
POST _bulk
{ "index": { "_index": "bookstore-rag-index", "_id": "2701" } }
{ "book_id": "2701", "title": "Moby Dick; Or, The Whale", "passage_text": "\"Moby Dick; Or, The Whale\" by Herman Melville is an epic novel published in 1851. Sailor Ishmael narrates the obsessive quest of Captain Ahab, who commands the whaling ship Pequod in pursuit of Moby Dick, a giant white sperm whale that destroyed his leg. Ahab's monomaniacal hunt for vengeance drives the ship and its diverse crew across the world's oceans, blending realistic whaling details with profound explorations of good, evil, fate, and human nature in this cornerstone of American literature. (This is an automatically generated summary.)" }
{ "index": { "_index": "bookstore-rag-index", "_id": "1342" } }
{ "book_id": "1342", "title": "Pride and Prejudice", "passage_text": "\"Pride and Prejudice\" by Jane Austen is a novel published in 1813. It follows Elizabeth Bennet, who must learn to see past first impressions and hasty judgments. With five daughters and an estate that can only pass to male heirs, the Bennet family faces financial pressure to marry well. When wealthy Mr. Darcy arrives in their countryside neighborhood, his pride and Elizabeth's prejudice set the stage for misunderstandings, hidden truths, and unexpected revelations about character and love. (This is an automatically generated summary.)" }
```

**Option B — full dataset:** body from [`rest/bulk/chapter-4-bookstore-rag-index.ndjson`](../../../rest/bulk/chapter-4-bookstore-rag-index.ndjson).

Allow several minutes for embedding. Then:

**Request** — paste into Dev Tools:


```http
POST bookstore-rag-index/_refresh
```

**Fast mode**  
`10-bulk-bookstore-rag-index.bru`


### **Step 8: k-NN search (stored query vector)**

**Why**  
Using a checked-in vector isolates index quality from query-time embedding. Open **`001-bookstore-rag-query-vector.json`** and paste the JSON array as **`"vector"`** below.

**Request** — paste into Dev Tools:

```http
GET bookstore-rag-index/_search
{
  "query": {
    "knn": {
      "passage_embedding": {
        "vector": [ /* paste 768 floats from 001-bookstore-rag-query-vector.json */ ],
        "k": 10
      }
    }
  },
  "profile": "true",
  "size": 10,
  "_source": ["title", "author", "price", "rating", "genre"]
}
```

**Expected** Nearest-neighbor hits with per-shard timing under **`profile`**.

**Fast mode**  
`11-knn-search.bru`


### **Step 9: Create hybrid search pipeline**

**Why**  
Rescale BM25 and k-NN scores before combining (weights **[0.3 keyword, 0.7 vector]**).

**Request** — paste into Dev Tools:

```http
PUT _search/pipeline/bookstore-hybrid-pipeline
{
  "description": "Hybrid search pipeline for bookstore RAG",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "arithmetic_mean",
          "parameters": {
            "weights": [0.3, 0.7]
          }
        }
      }
    }
  ]
}
```

**Fast mode**  
`12-create-hybrid-pipeline.bru`


### **Step 10: Hybrid search**

Paste the same query vector from **`001-bookstore-rag-query-vector.json`**:

**Request** — paste into Dev Tools:


```http
GET bookstore-rag-index/_search?search_pipeline=bookstore-hybrid-pipeline
{
  "_source": {
    "excludes": ["passage_embedding"]
  },
  "size": 10,
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "passage_text": {
              "query": "mystery novel under $20"
            }
          }
        },
        {
          "knn": {
            "passage_embedding": {
              "vector": [ /* paste from 001-bookstore-rag-query-vector.json */ ],
              "k": 10
            }
          }
        }
      ]
    }
  }
}
```

**Fast mode**  
`13-hybrid-search.bru`


### **Step 11: k-NN warmup and circuit breaker**

**Why**  
First queries pay a graph-load cost until HNSW structures sit in native memory. Warmup preloads them; the circuit breaker caps k-NN off-heap usage.

**Request** — paste into Dev Tools:

```http
GET _plugins/_knn/warmup/bookstore-rag-index
```

```http
GET _plugins/_knn/stats
```

Inspect **`graph_memory_usage_percentage`**, **`cache_hit_rate`**, **`graph_query_requests`**.

**Request** — paste into Dev Tools:


```http
PUT _cluster/settings
{
  "persistent": {
    "knn.memory.circuit_breaker.limit": "60%"
  }
}
```

**Fast mode**  
`14-knn-warmup.bru` → `15-knn-stats.bru` → `16-circuit-breaker.bru`

---

## What you learned

- End-to-end **RAG ingest**: pipeline → k-NN index → bulk with server-side embedding
- **k-NN** vs **hybrid** retrieval and why normalization pipelines matter
- **k-NN warmup** and memory circuit breaker tuning

## Next lesson

[Chapter 4 · Lesson 2](../Lesson%202/README.md) — index design, chunking, optimized bulk loading, shard sizing, and file preload.

## Reference scripts

| Script | Same as |
|--------|---------|
| `001-setup.py` | Steps 1–2 |
| `002-register-model.py` | Step 3 (+ poll) |
| `003-deploy-model.py` | Step 4 (+ poll) |
| `001a-establish-bookstore-rag.py` | Steps 5–7 (combined) |
| `001b-bookstore-rag-search.py` | Step 8 |
| `004-hybrid-search-pipeline.py` | Step 9 |
| `005-hybrid-search.py` | Step 10 |
| `005-prewarm.py` | Step 11 |

```bash
python 001-setup.py
python 002-register-model.py <model_group_id>
python 003-deploy-model.py <model_id>
python 001a-establish-bookstore-rag.py
python 001b-bookstore-rag-search.py
python 004-hybrid-search-pipeline.py
python 005-hybrid-search.py
python 005-prewarm.py
```
