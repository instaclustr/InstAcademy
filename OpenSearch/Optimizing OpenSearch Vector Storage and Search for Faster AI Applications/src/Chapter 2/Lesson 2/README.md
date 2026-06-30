# Chapter 2 · Lesson 2 — Ingesting data and running queries

**Chapter 2 · Lesson 2** — ingest pipeline embeddings, bulk-load the Gutendex dataset, and run hybrid neural + keyword search on **`vector-search-index`**.

← [Chapter 2 overview](../README.md) · [How to run labs](../../../HANDS-ON-GUIDE.md)

## Overview

### Goals

By the end of this lesson you will:

1. Create ingest pipeline **`vector-search-embeddings-pipeline`** with a **`text_embedding`** processor (**`passage_text` → `passage_embedding`**).
2. Create k-NN index **`vector-search-index`** with **`default_pipeline`** attached and **768-dimensional** vectors.
3. **Bulk-index** 256 books from the course dataset (embeddings generated automatically at ingest time).
4. Run a **hybrid-style** query combining **`neural`** (semantic) and **`match`** (lexical) scoring.

### Prerequisites

- Complete [Lesson 1](../Lesson%201/README.md) and set **`ML_MODEL_ID`** in **`src/.env`** (copy from **`src/.env.example`** if needed).
- Confirm **`src/sample-data.json`** exists ([Chapter 1 · Lesson 1](../../Chapter%201/Lesson%201/README.md)).
- Open **Dev Tools** (or Bruno fast mode: [`bruno/Chapter 2/Lesson 2/`](../../../bruno/Chapter%202/Lesson%202/)).

| Variable | Example | Used in |
|----------|---------|---------|
| `ML_MODEL_ID` | from Lesson 1 deploy | Pipeline, neural query |
| Index | `vector-search-index` | Bulk + search |
| Pipeline | `vector-search-embeddings-pipeline` | Default at index time |

**Order matters:** create the **pipeline** before the **index** — the index references the pipeline in **`default_pipeline`**.

---

## Lab steps

### **Step 1: Create the ingest pipeline**

**Why**  
The **`text_embedding`** processor calls your deployed model at index time, writing dense vectors into **`passage_embedding`** so clients send plain text only.

Replace **`YOUR_MODEL_ID`** with **`ML_MODEL_ID`** from **`src/.env`**.

**Request** — paste into Dev Tools:

```http
PUT _ingest/pipeline/vector-search-embeddings-pipeline
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

**Expected**

```json
{
  "acknowledged": true
}
```

**Fast mode**  
`bruno/Chapter 2/Lesson 2/01-create-ingest-pipeline.bru`


### **Step 2: Create the vector search index**

**Why each setting:**

- **`index.knn: true`** — enables k-NN query support for **`knn_vector`** fields.
- **`default_pipeline`** — every document indexed into this index runs through **`vector-search-embeddings-pipeline`** automatically.
- **`dimension: 768`** — must match **`msmarco-distilbert-base-tas-b`** output; mismatch causes ingest failures.

**Request** — paste into Dev Tools:

```http
PUT vector-search-index
{
  "settings": {
    "index.knn": true,
    "default_pipeline": "vector-search-embeddings-pipeline"
  },
  "mappings": {
    "properties": {
      "id": { "type": "text" },
      "passage_embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "engine": "lucene",
          "space_type": "l2",
          "name": "hnsw",
          "parameters": {}
        }
      },
      "passage_text": { "type": "text" }
    }
  }
}
```

**Expected**

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "vector-search-index"
}
```

If the index already exists from a previous run, delete it first: **`DELETE vector-search-index`**.

**Fast mode**  
`bruno/Chapter 2/Lesson 2/02-create-vector-search-index.bru`


### **Step 3: Bulk index the course dataset**

**Why**  
Bulk indexing amortizes network overhead. Each document triggers the **default ingest pipeline**, which embeds **`passage_text`** server-side using your deployed model. Expect this step to take **several minutes** on a trial cluster (one model inference per document).

The full bulk body (256 books) is in [`rest/bulk/chapter-2-lesson-2-vector-search-index.ndjson`](../../../rest/bulk/chapter-2-lesson-2-vector-search-index.ndjson). In Dev Tools:

1. Run the **`POST _bulk`** line below.
2. On the next line, paste the **entire contents** of that `.ndjson` file (no wrapping JSON — alternating action/source lines).
3. Ensure the request ends with a **blank line**.

**Request** — paste into Dev Tools:

```http
POST _bulk?timeout=60s
```

Each document includes **`passage_text`** (first Gutendex summary), plus **`id`**, **`title`**, **`authors`**, **`subjects`**, and **`bookshelves`**. Example opening lines from the bulk file:

```json
{"index": {"_index": "vector-search-index", "_id": "45304"}}
{"id": "45304", "title": "The City of God, Volume I", "authors": [{"name": "Augustine, of Hippo, Saint", "birth_year": 354, "death_year": 430}], "subjects": ["Apologetics -- Early works to 1800", "Kingdom of God -- Early works to 1800"], "passage_text": "\"The City of God, Volume I\" by Bishop of Hippo Saint Augustine is a work of Christian philosophy written in Latin in the early 5th century AD. ...", "bookshelves": ["Category: History - Ancient", "Category: Philosophy & Ethics", "Category: Religion/Spirituality"]}
{"index": {"_index": "vector-search-index", "_id": "84"}}
{"id": "84", "title": "Frankenstein; or, the modern prometheus", ...}
```

**Expected**

```json
{
  "errors": false,
  "items": [ ... ]
}
```

Check that **`errors`** is **`false`**. If any item reports an error, common causes are an **undeployed model**, wrong **`ML_MODEL_ID`**, or **dimension mismatch**.

**Alternative:** run **`python 003-ingest-data.py`** — it reads **`src/sample-data.json`** and builds the same bulk request programmatically.

**Fast mode**  
`bruno/Chapter 2/Lesson 2/03-bulk-ingest-books.bru` (body file points at the same `.ndjson`).


### **Step 4: Refresh the index (optional)**

**Why**  
OpenSearch is near-real-time. Refresh makes all bulk-indexed documents searchable immediately.

**Request** — paste into Dev Tools:

```http
POST vector-search-index/_refresh
```

**Expected**

```json
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  }
}
```


### **Step 5: Run hybrid neural + keyword search**

**Why**  
Semantic **`neural`** search handles paraphrases and intent; lexical **`match`** (BM25) handles exact terms. Combining both with **`script_score`** weights is a hand-rolled hybrid baseline (Chapter 3 introduces dedicated **`hybrid`** queries and score normalization).

Replace **`YOUR_MODEL_ID`** with **`ML_MODEL_ID`**. The query text matches the course example: *"historical fiction with an underdog story"*.

**Request** — paste into Dev Tools:

```http
GET vector-search-index/_search
{
  "_source": { "excludes": ["passage_embedding"] },
  "query": {
    "bool": {
      "filter": { "wildcard": { "id": "*1" } },
      "should": [
        {
          "script_score": {
            "query": {
              "neural": {
                "passage_embedding": {
                  "query_text": "historical fiction with an underdog story",
                  "model_id": "YOUR_MODEL_ID",
                  "k": 100
                }
              }
            },
            "script": { "source": "_score * 1.5" }
          }
        },
        {
          "script_score": {
            "query": {
              "match": { "passage_text": "historical fiction with an underdog story" }
            },
            "script": { "source": "_score * 1.7" }
          }
        }
      ]
    }
  }
}
```

**Expected** Hits under **`hits.hits`** with **`_score`**, **`title`**, and **`passage_text`** — **`passage_embedding`** excluded from **`_source`**. Titles related to historical or underdog narratives should rank highly.

**Fast mode**  
`bruno/Chapter 2/Lesson 2/04-neural-search.bru`

---

## What you learned

- How **`text_embedding`** ingest processors generate vectors at index time using **`ML_MODEL_ID`**.
- How **`default_pipeline`** ties an index to automatic embedding generation.
- How to combine **`neural`** and **`match`** queries for hybrid retrieval.

## Next lesson

- **Chapter 2 · Lesson 3 (theory only)** — choosing embedding processors — see [lessons without a lab folder](../../../HANDS-ON-GUIDE.md#lessons-without-a-lab-folder).
- **Hands-on cleanup:** [Lesson 4](../Lesson%204/README.md) — tear down **`vector-search-index`**, the pipeline, and optionally undeploy/delete the model.

## Reference scripts

| Script | Same as |
|--------|---------|
| `001-create-index-pipeline.py` | Step 1 (ingest pipeline) |
| `002-create-index.py` | Step 2 (vector index) |
| `003-ingest-data.py` | Step 3 (bulk from **`sample-data.json`**) |
| `004-search.py` | Step 5 (hybrid search) |
