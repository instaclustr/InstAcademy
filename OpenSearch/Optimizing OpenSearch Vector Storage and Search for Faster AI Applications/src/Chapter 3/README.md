# Chapter 3 — Mastering hybrid search in OpenSearch

**Chapter 3** · [Vector Storage & Search for AI](../../README.md)

← [Chapter 2](../Chapter%202/README.md) · [How to run labs](../../HANDS-ON-GUIDE.md) · **Next:** [Chapter 4](../Chapter%204/README.md)

No single retrieval method wins on its own. **Lexical BM25** nails exact terms but misses intent; **neural** search understands meaning but stumbles on rare jargon. **Hybrid search** runs both and merges the results, giving you precision *and* recall. This chapter builds a working hybrid pipeline end-to-end and compares two ways to merge results: **score normalization** and **Reciprocal Rank Fusion (RRF)**.

> **One combined workshop.** All three Chapter 3 lessons share the **same** sparse index and model, so they live in this single README. Build the foundation once in Lesson 3-1, then layer hybrid normalization (3-2) and RRF (3-3) on top. Run the steps top to bottom.

## What you build

| Lesson | You add | Key idea |
|--------|---------|----------|
| [3-1](#lesson-3-1--hybrid-search-how-it-works-and-why-it-matters) | Sparse model, ingest pipeline, sparse index, data — then run each method alone | Dense vs sparse vs lexical: see how each ranks the *same* query differently |
| [3-2](#lesson-3-2--creating-your-own-hybrid-search-in-opensearch) | `normalization-processor` search pipeline + `hybrid` query | Score-based fusion: rescale then weight-combine BM25 and sparse scores |
| [3-3](#lesson-3-3--enhance-search-accuracy-with-reciprocal-rank-fusion-rrf) | `score-ranker-processor` search pipeline + same `hybrid` query | Rank-based fusion: merge by rank position, no weight tuning needed |

## Prerequisites

- [Chapter 1 · Lesson 1](../Chapter%201/README.md) — cluster connectivity.
- [Chapter 2](../Chapter%202/README.md) — you deployed a **dense** model (`msmarco-distilbert-base-tas-b`) and built **`vector-search-index`**. **Keep both in place** — the dense comparison in Lesson 3-1 (Step 10) reuses them. If you tore them down, that one step is optional.
- A 3-node Instaclustr cluster with **ML Commons / AI Search** enabled.
- Open **OpenSearch Dashboards → Dev Tools** (Learn mode) or the **[Bruno `Chapter 3`](../../bruno/Chapter%203/)** collection (Fast mode).

**Save while you work** (notepad or Bruno environment):

| Variable | Set after | Used in |
|----------|-----------|---------|
| `model_group_id` | Step 2 | Step 3 (register sparse model) |
| `sparse_model_id` (`ML_MODEL_ID`) | Step 4 deploy | Steps 5, 9 (ingest + sparse/hybrid queries) |
| `dense_model_id` | Chapter 2 Lesson 1 | Step 10 (dense comparison only) |
| `task_id` | register / deploy | Polling |

> **Two models, two ids.** Chapter 3 uses a **sparse** encoding model; Chapter 2 used a **dense** one. Keep both ids straight (in Bruno: `sparseModelId` vs `modelId`).

**Query used throughout:** we run the *same* text — **`"a hero on a dangerous sea voyage"`** — against every method so you can line up the rankings side by side.

---

## Lesson 3-1 — Hybrid search: how it works and why it matters

**Goal:** understand *why* hybrid beats any single method, then prove it by building the sparse foundation and running **lexical**, **sparse**, and **dense** search in isolation on the same query.

### Concept: dense vs sparse vs lexical

- **Lexical (BM25)** scores documents by exact term overlap. Fast, transparent, great for names and codes — blind to synonyms and intent.
- **Dense embeddings** (Chapter 2) map text to a fixed-size vector (768 floats) in a continuous space and search with **k-NN**. They capture meaning but are opaque and every dimension costs memory.
- **Neural sparse embeddings** produce a *map* of token → weight where most values are zero. They encode token-level importance, index into an **inverted index** with the **`rank_features`** type, and can be *as efficient as BM25* while still adding semantic signal — a natural bridge between lexical and neural. That is why hybrid pipelines so often pair BM25 with **sparse** retrieval.

OpenSearch offers **two** processors to merge hybrid results, and this chapter uses both:

1. **`normalization-processor`** (Lesson 3-2) — *score-based*: rescales each sub-query's scores to a common range, then combines them with weights.
2. **`score-ranker-processor`** (Lesson 3-3) — *rank-based*: fuses results by their **rank position** using Reciprocal Rank Fusion.

> **Sparse model modes (worth knowing).** OpenSearch ships two families of pretrained sparse encoders:
> - **Bi-encoder** (e.g. `opensearch-neural-sparse-encoding-v1` / `-v2-distill`) runs the model at **both** index and query time — you must pass a `model_id` on every query. **This workshop uses the bi-encoder v1** for continuity with the existing lab assets.
> - **Doc-only** (e.g. `opensearch-neural-sparse-encoding-doc-v2-distill`, `-doc-v3-distill`, `-doc-v3-gte`) runs the model only at **index** time; at query time it just tokenizes with a lightweight analyzer, so search is cheaper. Doc-only queries use `query_text` + an `analyzer` (default `bert-uncased`) **instead of** `model_id`.
>
> The video mentions `opensearch-neural-sparse-encoding-doc-v3` — that is a doc-only model. Everything below works with either family; only the **query** clause in Step 9 changes (`model_id` for bi-encoder vs `analyzer` for doc-only). We keep v1 bi-encoder so the query stays explicit and easy to trace.

### **Step 1: Enable URL model registration**

**Why**
ML Commons blocks fetching model artifacts from a URL until you opt in. This is a one-time persistent cluster setting (already on if you did Chapter 2).

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

**Fast mode** `bruno/Chapter 3/01-enable-url-model-registration.bru`


### **Step 2: Register a model group (skip if you have one)**

**Why**
Every registered model belongs to a group for access control and versioning. **Reuse the `huggingface-models` group from Chapter 2** if it exists — copy its `model_group_id` and skip to Step 3.

**Request** — paste into Dev Tools:

```http
POST _plugins/_ml/model_groups/_register
{
  "name": "huggingface-models",
  "description": "A group for Hugging Face transformer models"
}
```

**Save** `model_group_id` from the response.

**Fast mode** `bruno/Chapter 3/02-register-model-group.bru`


### **Step 3: Register the neural sparse encoding model**

**Why**
This model turns text into sparse token→weight maps (not 768-dim dense vectors). Registration downloads the artifact asynchronously and returns a `task_id`.

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

**Expected** JSON with a `task_id`.

**Poll until registration completes:**

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

Repeat every few seconds until `"state": "COMPLETED"`. On `FAILED`, check cluster logs and node disk/memory.

**Save** `model_id` from the completed task — this is your **`sparse_model_id`**.

**Fast mode** `bruno/Chapter 3/03-register-sparse-model.bru` → `bruno/Chapter 3/04-poll-register-task.bru`


### **Step 4: Deploy the sparse model**

**Why**
Deploy loads the model weights into ML-node memory so ingest pipelines and `neural_sparse` queries can call it.

Replace `YOUR_SPARSE_MODEL_ID`:

**Request** — paste into Dev Tools:

```http
POST _plugins/_ml/models/YOUR_SPARSE_MODEL_ID/_deploy
```

Poll again if deploy returns a `task_id`:

```http
GET _plugins/_ml/tasks/YOUR_TASK_ID
```

**Save** write down the sparse model id (in Bruno, set **`sparseModelId`** in the **Local** environment).

**Fast mode** `bruno/Chapter 3/05-deploy-sparse-model.bru` → `bruno/Chapter 3/06-poll-deploy-task.bru`


### **Step 5: Create the sparse ingest pipeline**

**Why**
This pipeline runs on every document at index time. It **chunks** long `passage_text` into small token windows, then **sparse-encodes** each chunk into a nested `passage_embedding` object. Create it **before** the index so the index can reference it.

- **`text_chunking` / `fixed_token_length`** splits by token count. **`token_limit: 5`** is intentionally tiny so you can *see* multiple chunks per book in lab responses; production uses 128–512.
- **`overlap_rate: 0.5`** keeps phrases that straddle a chunk boundary intact in at least one chunk.
- **`sparse_encoding`** calls your deployed model. **`prune_type: max_ratio` / `prune_ratio: 0.1`** drops tokens weighted below 10% of the max to keep vectors small.

Replace `YOUR_SPARSE_MODEL_ID`:

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
        "model_id": "YOUR_SPARSE_MODEL_ID",
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

**Expected** `"acknowledged": true`

**Fast mode** `bruno/Chapter 3/07-create-sparse-ingest-pipeline.bru`


### **Step 6: Create the sparse index**

**Why each mapping choice:**

- **`default_pipeline`** — every document indexed here runs `nlp-ingest-pipeline` automatically, so clients send plain text only.
- **`rank_features`** on `sparse_encoding` — the sparse model emits **string** token keys; the `sparse_vector` type only accepts numeric keys and would fail at index time with `[sparse_vector] fields should be valid integer`.
- **`nested`** on `passage_embedding` — each chunk becomes an independently queryable sub-document, so a query can score the single **best** chunk per book (`score_mode: max`).

If you are re-running, delete first (mappings are mostly immutable):

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
      "number_of_replicas": 1,
      "default_pipeline": "nlp-ingest-pipeline"
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

**Fast mode** `bruno/Chapter 3/08-delete-sparse-index.bru` (optional) → `bruno/Chapter 3/09-create-sparse-index.bru`


### **Step 7: Bulk index the sample books**

**Why**
Each document triggers chunking + sparse encoding **inside** the cluster (one model inference per chunk), so this is slower than a plain bulk. Allow several minutes for the full file.

The full body is in [`rest/bulk/chapter-3-lesson-1-sparse-index.ndjson`](../../rest/bulk/chapter-3-lesson-1-sparse-index.ndjson) (indexes into `my-sparse-neural-index`). In Dev Tools, run `POST _bulk`, then paste the **entire file contents** as the body (alternating action/source lines), ending with a blank line.

**Request** — paste into Dev Tools:

```http
POST _bulk?timeout=600s
```

*(then paste the NDJSON body)*

**Quick smoke test instead** (2 books, if you just want to reach a searchable state fast):

```http
POST _bulk
{ "index": { "_index": "my-sparse-neural-index", "_id": "84" } }
{ "id": "84", "title": "Frankenstein; or, the modern prometheus", "passage_text": "\"Frankenstein; Or, The Modern Prometheus\" by Mary Wollstonecraft Shelley is a Gothic novel published in 1818. Victor Frankenstein creates a living creature from assembled body parts, then flees in horror when it awakens. The abandoned creature learns language, seeks connection, faces repeated rejection, and confronts his creator with a desperate demand that sets both on a path of vengeance and tragedy." }
{ "index": { "_index": "my-sparse-neural-index", "_id": "2701" } }
{ "id": "2701", "title": "Moby Dick; Or, The Whale", "passage_text": "\"Moby Dick; Or, The Whale\" by Herman Melville is an epic novel published in 1851. Sailor Ishmael narrates the obsessive quest of Captain Ahab, who commands the whaling ship Pequod on a dangerous sea voyage in pursuit of the giant white whale that destroyed his leg, blending realistic whaling detail with meditations on fate, vengeance, and human nature." }
```

**Expected** `"errors": false`. If any item errors, the usual causes are an **undeployed model**, wrong **`model_id`** in Step 5, or the sparse field mapped as `sparse_vector` instead of `rank_features`.

> **If items fail with `Model not ready yet` or `Failed to get data object from index .plugins-ml-model`:** the model is not fully deployed on every ML node — common on trial clusters under load or after node churn. Check `GET _plugins/_ml/models/YOUR_SPARSE_MODEL_ID` and confirm `model_state` is `DEPLOYED` (not `PARTIALLY_DEPLOYED` or `DEPLOY_FAILED`). If it isn't, re-run the deploy from Step 5, wait for the task to reach `COMPLETED`, then delete and recreate the index (Steps 6–7 ordering) and retry the bulk. This is standard ML Commons behavior, not a problem with your request.

Refresh so hits are immediately searchable:

```http
POST my-sparse-neural-index/_refresh
```

**Fast mode** `bruno/Chapter 3/10-bulk-sparse-index.bru` → `bruno/Chapter 3/11-refresh-sparse-index.bru`


### **Step 8: Lexical-only baseline (BM25)**

**Why**
Establish the keyword-only ranking first. A plain `match` scores documents purely on term overlap — no model involved.

**Request** — paste into Dev Tools:

```http
GET my-sparse-neural-index/_search
{
  "_source": { "excludes": ["passage_embedding", "passage_chunk"] },
  "size": 5,
  "query": {
    "match": {
      "passage_text": "a hero on a dangerous sea voyage"
    }
  }
}
```

**Expected** Up to 5 hits ordered by BM25 `_score`. Books that literally contain words like *voyage*, *sea*, *dangerous* float up; thematically similar books that use different words are missed.

**Save** the **top-5 titles and order** — you will compare against sparse, dense, hybrid, and RRF.

**Fast mode** `bruno/Chapter 3/12-lexical-search.bru`


### **Step 9: Sparse-only (`neural_sparse`)**

**Why**
Now retrieve by *meaning* using the sparse model. `neural_sparse` encodes the query text with your `sparse_model_id` and matches it against the `rank_features` field. The `nested` wrapper with `score_mode: max` gives each book the score of its single best-matching chunk.

Replace `YOUR_SPARSE_MODEL_ID`:

**Request** — paste into Dev Tools:

```http
GET my-sparse-neural-index/_search
{
  "_source": { "excludes": ["passage_embedding", "passage_chunk"] },
  "size": 5,
  "query": {
    "nested": {
      "path": "passage_embedding",
      "score_mode": "max",
      "query": {
        "neural_sparse": {
          "passage_embedding.sparse_encoding": {
            "query_text": "a hero on a dangerous sea voyage",
            "model_id": "YOUR_SPARSE_MODEL_ID"
          }
        }
      }
    }
  }
}
```

> **Doc-only variant.** If you registered a `...-encoding-doc-*` model, drop `model_id` and use `"analyzer": "bert-uncased"` instead — the two are mutually exclusive.

**Expected** Up to 5 hits. Ranking differs from Step 8: books that are *about* perilous journeys or heroism rank well even when they don't use those exact words.

**Save** the **top-5 order** and compare to the lexical list. Note which books appear in one list but not the other — that gap is exactly what hybrid search closes.

**Fast mode** `bruno/Chapter 3/13-sparse-search.bru`


### **Step 10: Dense-only comparison (optional — reuses Chapter 2)**

**Why**
Round out the picture with dense k-NN. This runs against **Chapter 2's** `vector-search-index` and dense model, so you can see all three retrieval styles on the same query. **Skip if you tore Chapter 2 down.**

Replace `YOUR_DENSE_MODEL_ID` with your **Chapter 2** model id (not the sparse one):

**Request** — paste into Dev Tools:

```http
GET vector-search-index/_search
{
  "_source": { "excludes": ["passage_embedding"] },
  "size": 5,
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "a hero on a dangerous sea voyage",
        "model_id": "YOUR_DENSE_MODEL_ID",
        "k": 10
      }
    }
  }
}
```

**Expected** Up to 5 semantically ranked hits. Dense and sparse often agree on *theme* but disagree on exact order — neither alone matches keyword precision. That is the motivation for hybrid.

**Save** the **top-5 order** alongside your lexical and sparse lists — Lesson 3-3 asks you to line all three up against the RRF ranking.

**Fast mode** `bruno/Chapter 3/14-dense-search-compare.bru`

---

## Lesson 3-2 — Creating your own hybrid search in OpenSearch

**Goal:** run BM25 and sparse retrieval **together** in one `hybrid` query, and merge their scores with a `normalization-processor` search pipeline. Compare the blended ranking against the single-method lists from Lesson 3-1.

### Why a search pipeline is required

BM25 scores (~0–20) and sparse scores (~0–10) live on different scales. Add them directly and whichever branch produces larger numbers dominates. A **search pipeline** with a `normalization-processor` fixes this: its `phase_results_processors` run **after** each sub-query gathers its own hits but **before** OpenSearch merges them — exactly the moment to rescale.

- **`normalization.technique`** — `min_max` rescales each branch to [0, 1]. (Also valid: `l2`, and `z_score`.)
- **`combination.technique`** — `arithmetic_mean` = weighted average. (Also valid: `geometric_mean`, `harmonic_mean`. `z_score` supports only `arithmetic_mean`.)
- **`weights`** — one per sub-query, must sum to **1.0**. Here `[0.3, 0.7]` trusts the sparse branch more than keyword.

### **Step 1: Create the normalization search pipeline**

**Why**
This turns the theory above into a reusable cluster object. The pipeline lives on the cluster (not in any one query), so every hybrid search that references it by name gets the same min–max rescaling and 30/70 weighting — change the weights once here and every caller picks it up. Creating it **before** running a `hybrid` query matters: without it, the two branches' raw scores are simply summed and the larger scale wins.

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

**Fast mode** `bruno/Chapter 3/15-create-normalization-pipeline.bru`


### **Step 2: Run the hybrid query (normalized)**

**Why**
The `hybrid` query runs each sub-query independently, then the pipeline named in `?search_pipeline=` normalizes and combines their scores. A `hybrid` query supports **up to 5** sub-queries; here we use two (lexical + sparse). The `weights` order matches the `queries` order: index 0 → the `match`, index 1 → the `neural_sparse`.

Replace `YOUR_SPARSE_MODEL_ID`:

**Request** — paste into Dev Tools:

```http
GET my-sparse-neural-index/_search?search_pipeline=nlp-search-normalization-pipeline
{
  "_source": { "excludes": ["passage_embedding", "passage_chunk"] },
  "size": 5,
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "passage_text": {
              "query": "a hero on a dangerous sea voyage"
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
                  "query_text": "a hero on a dangerous sea voyage",
                  "model_id": "YOUR_SPARSE_MODEL_ID"
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

**Expected** Up to 5 hits ranked by the **combined normalized** score. Compare this order to your Step 8 (lexical) and Step 9 (sparse) lists: hybrid typically pulls the best of both — keyword-exact hits *and* thematically relevant ones — toward the top.

**Save** the **top-5 order**; you will compare it against the RRF ranking in Lesson 3-3.

**Fast mode** `bruno/Chapter 3/16-hybrid-normalized-search.bru`


### **Step 3: Feel the knobs (optional)**

Re-run Step 2 after editing the pipeline to build intuition:

- Flip the weights to `[0.7, 0.3]` (favor keyword) and re-run — watch keyword-exact books climb.
- Change `normalization.technique` to `l2` — a different rescaling shape shifts the blend.

Re-`PUT` the pipeline, then re-run the query. No re-indexing needed — search pipelines only affect query time.

---

## Lesson 3-3 — Enhance search accuracy with Reciprocal Rank Fusion (RRF)

**Goal:** merge the same two branches by **rank position** instead of score, using the `score-ranker-processor`. Compare the RRF ranking to the normalized one.

### What RRF is and why you'd use it

Reciprocal Rank Fusion ignores raw scores entirely and fuses results by **where** each document ranks in each result list:

```
rankScore(doc) = Σ  1 / (k + rank_j)
                 j
```

where `rank_j` is the document's position in result list *j* and `k` is the **rank constant**. A document ranked highly in several lists accumulates a large reciprocal-rank sum. Because it uses ranks, not scores, RRF **needs no score normalization and no labeled data to tune** — it just works.

- **`rank_constant`** (default **60**) softens the advantage of top ranks. **Larger** `k` → scores more uniform, top hits matter less; **smaller** `k` → bigger gaps between ranks. We use `40`.
- **Trade-off:** RRF trades a little peak precision for simplicity and robustness. If you have the resources to tune weights with labeled data, score-based normalization (3-2) can edge it out; for most workloads RRF delivers strong results with minimal config.
- `weights` are still supported (one per sub-query, summing to 1.0) if you want to bias one branch.

### **Step 1: Create the RRF search pipeline**

**Why**
Same pipeline slot (`phase_results_processors`) as normalization, but a **rank-based** processor. `technique: "rrf"` selects Reciprocal Rank Fusion.

**Request** — paste into Dev Tools:

```http
PUT _search/pipeline/rrf-search-pipeline
{
  "description": "Post processor for hybrid RRF search",
  "phase_results_processors": [
    {
      "score-ranker-processor": {
        "combination": {
          "technique": "rrf",
          "rank_constant": 40,
          "parameters": {
            "weights": [0.7, 0.3]
          }
        }
      }
    }
  ]
}
```

**Expected** `"acknowledged": true`

**Fast mode** `bruno/Chapter 3/17-create-rrf-pipeline.bru`


### **Step 2: Run the hybrid query through RRF**

**Why**
The query body is **identical** to Lesson 3-2 Step 2 — only the `search_pipeline` changes. That is the point: the *same* two branches, fused a different way. Compare rankings to see how rank-based fusion differs from score-based.

Replace `YOUR_SPARSE_MODEL_ID`:

**Request** — paste into Dev Tools:

```http
GET my-sparse-neural-index/_search?search_pipeline=rrf-search-pipeline
{
  "_source": { "excludes": ["passage_embedding", "passage_chunk"] },
  "size": 5,
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "passage_text": {
              "query": "a hero on a dangerous sea voyage"
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
                  "query_text": "a hero on a dangerous sea voyage",
                  "model_id": "YOUR_SPARSE_MODEL_ID"
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

**Expected** Up to 5 hits ranked by fused reciprocal rank. `_score` values are small (RRF sums of `1/(k+rank)`), unlike the [0,1]-ish normalized scores. The **order** may match or diverge from Step 2 of Lesson 3-2 — RRF is less sensitive to outlier scores, so a document that ranks decently in *both* lists can overtake one that scored very high in only one.

**Compare all five:** line up your saved top-5 lists — **lexical** (3-1 Step 8), **sparse** (3-1 Step 9), **dense** (3-1 Step 10), **hybrid-normalized** (3-2), **hybrid-RRF** (3-3). This side-by-side is the whole lesson: no single method is complete, and the two fusion strategies produce meaningfully different rankings.

**Fast mode** `bruno/Chapter 3/18-hybrid-rrf-search.bru`

---

## What you learned

- **Why hybrid wins:** lexical, dense, and sparse each rank the same query differently; fusing them recovers precision *and* recall.
- **Neural sparse** encodings (`rank_features` + `nested`) bridge lexical and neural, and why bi-encoder vs doc-only changes only the query clause.
- **Score-based fusion** with `normalization-processor` — rescale, then weight-combine (`min_max` + `arithmetic_mean`).
- **Rank-based fusion** with `score-ranker-processor` — RRF merges by rank position with a single `rank_constant`, no weight tuning required.
- A `hybrid` query runs **up to 5** sub-queries; the merge behavior lives entirely in the **search pipeline**, so you can swap fusion strategies without touching the query or the index.

## Cleanup

Run when you are done to free cluster resources.

```http
DELETE _search/pipeline/nlp-search-normalization-pipeline
```
```http
DELETE _search/pipeline/rrf-search-pipeline
```
```http
DELETE my-sparse-neural-index
```
```http
DELETE _ingest/pipeline/nlp-ingest-pipeline
```

Optionally undeploy and delete the sparse model (frees ML-node memory):

```http
POST _plugins/_ml/models/YOUR_SPARSE_MODEL_ID/_undeploy
```
```http
DELETE _plugins/_ml/models/YOUR_SPARSE_MODEL_ID
```

**Fast mode** `bruno/Chapter 3/19-cleanup.bru` (delete pipelines + index).

Leave Chapter 2's `vector-search-index` and dense model in place if you plan to continue to Chapter 4.

## Next chapter

[Chapter 4 · Lesson 1](../Chapter%204/README.md) — bookstore **RAG** with dense k-NN and hybrid search.
