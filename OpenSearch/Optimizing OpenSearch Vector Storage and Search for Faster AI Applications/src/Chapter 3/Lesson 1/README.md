# Chapter 3 Lesson 1 — Neural sparse encoding and hybrid search

**InstAcademy → OpenSearch:** Lessons **3-1** through **3-3** · [Optimizing OpenSearch Vector Storage and Search for Faster AI Applications](../../../OpenSearch%20Learning%20Path%201.docx) — hybrid search rationale, sparse vector index + ML Commons, and score normalization for accurate hybrid ranking.

## Overview

### Goals

By the end of this lesson you will:

1. Register and deploy **`amazon/neural-sparse/opensearch-neural-sparse-encoding-v1`**
2. Create **`nlp-search-normalization-pipeline`** (rescales BM25 vs sparse scores before combining)
3. Create **`my-sparse-neural-index`** with **nested** **`rank_features`** sparse encodings per chunk
4. Attach **`nlp-ingest-pipeline`** (text chunking + sparse encoding)
5. Bulk-load books from **`src/sample-data.json`**
6. Run a **`hybrid`** query (BM25 + **`neural_sparse`**) with the search pipeline

**Why neural sparse?** Dense vectors (Chapter 2) excel at semantic similarity but are opaque. Sparse encoders produce token→weight maps you can inspect; they often handle rare terms and paraphrases better than pure BM25 while staying cheaper than full dense search at scale.

### Prerequisites

- Complete [Chapter 1 Lesson 1](../../Chapter%201/1-1/README.md) and [Chapter 2 Lesson 1](../../Chapter%202/Lesson%201/README.md) (or equivalent ML bootstrap).
- Open **Dev Tools** (or Bruno: [`bruno/Chapter 3/Lesson 1/`](../../../bruno/Chapter%203/Lesson%201/)).
- Keep a notepad for **`model_group_id`**, **`model_id`**, **`task_id`**, and add **`ML_MODEL_ID=<model_id>`** to **`src/.env`** after deploy.

| Variable | Used in |
|----------|---------|
| `model_group_id` | Step 2 (register sparse model) |
| `model_id` / `ML_MODEL_ID` | Steps 3, 7, 9 (ingest + query) |
| `task_id` | Poll after register/deploy |

---

## Lab steps

### **Step 1: Enable URL model registration**

**Why**  
ML Commons blocks fetching model artifacts from URLs until you opt in.

**Request** — paste into Dev Tools:

```http
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.allow_registering_model_via_url": true
  }
}
```

**Expected** `"acknowledged": true`

**Fast mode**  
`bruno/Chapter 3/Lesson 1/02-enable-url-model-registration.bru`


### **Step 2: Register model group (skip if you have one)**

**Why**  
Every registered model belongs to a group for access control and versioning. Reuse the **`huggingface-models`** group from Chapter 2 if it already exists — copy its **`model_group_id`** and skip to Step 3.

**Request** — paste into Dev Tools:

```http
POST _plugins/_ml/model_groups/_register
{
  "name": "huggingface-models",
  "description": "A group for Hugging Face transformer models"
}
```

**Save:** **`model_group_id`** from the response.

**Fast mode**  
`bruno/Chapter 3/Lesson 1/03-register-model-group.bru`


### **Step 3: Register the neural sparse encoding model**

**Why**  
This model turns text into sparse token weights (not 768-dim dense vectors). Registration downloads the artifact asynchronously.

Replace `YOUR_MODEL_GROUP_ID`:

**Request** — paste into Dev Tools:

```http
POST _plugins/_ml/models/_register
{
  "name": "amazon/neural-sparse/opensearch-neural-sparse-encoding-v1",
  "version": "1.0.1",
  "model_group_id": "YOUR_MODEL_GROUP_ID",
  "model_format": "TORCH_SCRIPT"
}
```

**Expected** JSON with **`task_id`** and/or **`model_id`**.

#### **Poll until registration completes**

If you received a **`task_id`**:

**Request** — paste into Dev Tools:

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

Repeat every few seconds until **`"state": "COMPLETED"`**. On **`FAILED`**, check cluster logs and disk/memory.

**Save:** **`model_id`** from the completed task or register response.

**Fast mode**  
`04-register-sparse-model.bru` → `05-poll-ml-task.bru`


### **Step 4: Deploy the sparse model**

**Why**  
Deploy loads weights into ML node memory so ingest pipelines and **`neural_sparse`** queries can call the model.

Replace `YOUR_MODEL_ID`:

**Request** — paste into Dev Tools:

```http
POST _plugins/_ml/models/YOUR_MODEL_ID/_deploy
```

Poll again if deploy returns a **`task_id`**:

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

**Save:** add **`ML_MODEL_ID=YOUR_MODEL_ID`** to **`src/.env`**.

**Fast mode**  
`06-deploy-model.bru` → `07-poll-ml-task-deploy.bru`


### **Step 5: Create the hybrid search pipeline (Course 3-1 / 3-3)**

**Why**  
BM25 scores (~0–20) and sparse scores (~0–10) live on different scales. Without normalization, whichever branch produces larger numbers dominates. This pipeline rescales each branch to [0, 1], then combines with weights **[0.3 keyword, 0.7 sparse]**.

**Request** — paste into Dev Tools:

```http
PUT _search/pipeline/nlp-search-normalization-pipeline
{
  "description": "Post processor for hybrid search",
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

**Expected** `"acknowledged": true`

**Fast mode**  
`bruno/Chapter 3/Lesson 1/08-create-search-pipeline.bru`


### **Step 6: Create the sparse neural index (Course 3-2)**

**Why each mapping choice:**

- **`rank_features`** on **`sparse_encoding`** — the sparse model emits string token keys; **`sparse_vector`** only accepts numeric keys and will fail at index time.
- **`nested`** on **`passage_embedding`** — each chunk gets its own sparse map; queries can score the best chunk per document (`score_mode: max`).

Delete first if re-running (mappings are mostly immutable):

**Request** — paste into Dev Tools:

```http
DELETE my-sparse-neural-index
```

Then create:

```http
PUT my-sparse-neural-index
{
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  },
  "mappings": {
    "properties": {
      "passage_text": { "type": "text" },
      "passage_chunk": { "type": "text" },
      "passage_embedding": {
        "type": "nested",
        "properties": {
          "sparse_encoding": { "type": "rank_features" }
        }
      }
    }
  }
}
```

**Expected** `"acknowledged": true`

**Fast mode**  
`bruno/Chapter 3/Lesson 1/09-delete-sparse-index.bru` (optional) → `10-create-sparse-index.bru`


### **Step 7: Create the sparse ingest pipeline**

**Why**  
Chunk long **`passage_text`** into small windows, then sparse-encode each chunk into nested **`passage_embedding`**. The **`token_limit: 5`** is intentionally tiny so you can see multiple chunks per book in lab responses; production apps typically use 128–512.

Replace `YOUR_MODEL_ID` with **`ML_MODEL_ID`** from **`src/.env`**:

**Request** — paste into Dev Tools:

```http
PUT _ingest/pipeline/nlp-ingest-pipeline
{
  "description": "A sparse encoding ingest pipeline",
  "processors": [
    {
      "text_chunking": {
        "algorithm": {
          "fixed_token_length": {
            "token_limit": 5,
            "overlap_rate": 0.5,
            "tokenizer": "standard"
          }
        },
        "field_map": {
          "passage_text": "passage_chunk"
        }
      }
    },
    {
      "sparse_encoding": {
        "model_id": "YOUR_MODEL_ID",
        "prune_type": "max_ratio",
        "prune_ratio": 0.1,
        "field_map": {
          "passage_chunk": "passage_embedding"
        }
      }
    }
  ]
}
```

Attach as the index default pipeline:

**Request** — paste into Dev Tools:


```http
PUT my-sparse-neural-index/_settings
{
  "index": {
    "default_pipeline": "nlp-ingest-pipeline"
  }
}
```

**Expected** both calls return `"acknowledged": true`

**Fast mode**  
`11-create-ingest-pipeline.bru` → `12-attach-default-pipeline.bru`


### **Step 8: Bulk index sample books**

**Why**  
Each document triggers chunking + sparse encoding inside the cluster. A single bulk of ~256 books can take several minutes.

**Option A — small inline smoke test (2 books):**

**Request** — paste into Dev Tools:

```http
POST _bulk
{ "index": { "_index": "my-sparse-neural-index", "_id": "84" } }
{ "id": "84", "title": "Frankenstein; or, the modern prometheus", "passage_text": "\"Frankenstein; Or, The Modern Prometheus\" by Mary Wollstonecraft Shelley is a Gothic novel published in 1818. It tells the story of Victor Frankenstein, a young scientist who creates a living creature from assembled body parts in an unorthodox experiment. When the creature awakens, Victor flees in horror, abandoning his creation. The conscious being must navigate a world that fears him, learning language and seeking connection, only to face repeated rejection. Embittered and alone, the creature confronts his creator with a desperate request that will set both on a dark path of vengeance and tragedy. (This is an automatically generated summary.)" }
{ "index": { "_index": "my-sparse-neural-index", "_id": "2701" } }
{ "id": "2701", "title": "Moby Dick; Or, The Whale", "passage_text": "\"Moby Dick; Or, The Whale\" by Herman Melville is an epic novel published in 1851. Sailor Ishmael narrates the obsessive quest of Captain Ahab, who commands the whaling ship Pequod in pursuit of Moby Dick, a giant white sperm whale that destroyed his leg. Ahab's monomaniacal hunt for vengeance drives the ship and its diverse crew across the world's oceans, blending realistic whaling details with profound explorations of good, evil, fate, and human nature in this cornerstone of American literature. (This is an automatically generated summary.)" }
```

**Option B — full course dataset:** paste the NDJSON from [`rest/bulk/chapter-3-lesson-1-sparse-index.ndjson`](../../../rest/bulk/chapter-3-lesson-1-sparse-index.ndjson) into Dev Tools as the body of `POST _bulk` (same format as Option A — action line, source line, repeat).

**Expected** `"errors": false` after encoding completes. Allow several minutes for the full file.

Refresh when done:

**Request** — paste into Dev Tools:

```http
POST my-sparse-neural-index/_refresh
```

**Fast mode**  
`bruno/Chapter 3/Lesson 1/13-bulk-sparse-index.bru` (body file → `rest/bulk/chapter-3-lesson-1-sparse-index.ndjson`)


### **Step 9: Run hybrid + neural_sparse search**

**Why**  
The **`hybrid`** query runs BM25 and sparse retrieval independently; **`?search_pipeline=nlp-search-normalization-pipeline`** rescales and combines scores. **`nested`** + **`score_mode: max`** means each book’s score comes from its single best-matching chunk.

Replace `YOUR_MODEL_ID`:

**Request** — paste into Dev Tools:

```http
GET my-sparse-neural-index/_search?search_pipeline=nlp-search-normalization-pipeline
{
  "_source": {
    "excludes": ["passage_embedding"]
  },
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "passage_text": {
              "query": "a hero"
            }
          }
        },
        {
          "nested": {
            "path": "passage_embedding",
            "score_mode": "max",
            "query": {
              "neural_sparse": {
                "passage_embedding.sparse_encoding": {
                  "query_text": "a hero",
                  "model_id": "YOUR_MODEL_ID"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

**Expected**  
Hits ranked by combined normalized score; Moby Dick / hero-themed summaries often rank highly depending on your bulk data.

Try changing query text to **`whale`** or hybrid weights in Step 5 to feel ranking shift.

**Fast mode**  
`bruno/Chapter 3/Lesson 1/14-hybrid-sparse-search.bru`

---

## What you learned

- How **neural sparse** encodings differ from dense **`knn_vector`** fields
- Why **`rank_features`** + **`nested`** are required for chunked sparse search
- How a **search pipeline** fixes hybrid score-scale mismatch
- The **`hybrid`** query + **`neural_sparse`** pattern for production-style retrieval

## Next chapter

[Chapter 4 Lesson 1](../../Chapter%204/Lesson%201/README.md) — bookstore **RAG** with **`all-mpnet-base-v2`**, dense k-NN, and hybrid search.

## Reference scripts

Run from this folder after `pip install -r ../../../requirements.txt`:

| Script | Same as |
|--------|---------|
| `001-setup.py` | Steps 1–2 |
| `001a-register-model.py` | Step 3 (+ poll) |
| `001b-deploy-model.py` | Step 4 (+ poll) |
| `002-post-processing-pipeline.py` | Step 5 |
| `003-sparse-data-index.py` | Step 6 |
| `004-sparse-ingest-pipeline.py` | Step 7 |
| `005-load-data.py` | Step 8 (full bulk from `src/sample-data.json`) |
| `006-search.py` | Step 9 |

Recommended order:

```bash
python 001-setup.py
python 001a-register-model.py <model_group_id>
python 001b-deploy-model.py <model_id>
python 002-post-processing-pipeline.py
python 003-sparse-data-index.py
python 004-sparse-ingest-pipeline.py
python 005-load-data.py
python 006-search.py
```
