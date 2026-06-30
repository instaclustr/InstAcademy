# Chapter 4 · Lesson 3 — Query optimization for RAG pipelines

**Chapter 4 · Lesson 3** — debug relevance with **explain**, measure quality with **`_rank_eval`**, and enforce business rules (in-stock) via **search pipelines**.

← [Chapter 4 overview](../README.md) · [How to run labs](../../../HANDS-ON-GUIDE.md)

## Overview

### Goals

By the end of this lesson you will:

1. Run **hybrid** search with **`explain: true`** and read score breakdowns
2. Score search quality with **`_rank_eval`** (MRR @ 10)
3. Create a teaching **search pipeline** with **`script_score`** (intentionally imperfect)
4. Set a **default search pipeline** on an index
5. Build **`bookstore-full-pipeline`** — stock filter + hybrid normalization combined

### Prerequisites

- Complete [Chapter 4 · Lesson 1](../Lesson%201/README.md) and [Lesson 2](../Lesson%202/README.md) — index **`bookstore-rag`**, pipeline **`bookstore-hybrid-pipeline`**, data loaded
- Open **`001-bookstore-rag-query-vector.json`** in this folder (768-dim query vector for k-NN branches)
- Open **Dev Tools** (or Bruno: [`bruno/Chapter 4/Lesson 3/`](../../../bruno/Chapter%204/Lesson%203/))

---

## Lab steps

### **Step 1: Explain hybrid search scores**

**Why**  
When ranking feels wrong, **`_explanation`** shows BM25 term weights, vector similarity, and normalization contributions per hit. Expensive — use for debugging only.

Paste the query vector from **`001-bookstore-rag-query-vector.json`**:

**Request** — paste into Dev Tools:

```http
GET bookstore-rag/_search?search_pipeline=bookstore-hybrid-pipeline&explain=true
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "content": {
              "query": "whale"
            }
          }
        },
        {
          "knn": {
            "content_embedding": {
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

**Expected** Each hit includes **`_explanation`** — a tree of sub-scorers and values.

**Fast mode**  
`bruno/Chapter 4/Lesson 3/01-explain-hybrid-search.bru`


### **Step 2: Rank evaluation (MRR @ 10)**

**Why**  
**`_rank_eval`** turns labeled relevance judgments into a single metric you can optimize when tuning hybrid weights, chunk size, or models.

Replace the vector array as in Step 1:

**Request** — paste into Dev Tools:

```http
GET bookstore-rag/_rank_eval
{
  "requests": [
    {
      "id": "mystery_query",
      "request": {
        "query": {
          "hybrid": {
            "queries": [
              {
                "match": {
                  "content": {
                    "query": "whale"
                  }
                }
              },
              {
                "knn": {
                  "content_embedding": {
                    "vector": [ /* paste from 001-bookstore-rag-query-vector.json */ ],
                    "k": 10
                  }
                }
              }
            ]
          }
        }
      },
      "ratings": [
        {
          "_index": "bookstore-rag",
          "_id": "2701",
          "rating": 0
        }
      ]
    }
  ],
  "metric": {
    "mean_reciprocal_rank": {
      "k": 10,
      "relevant_rating_threshold": 1
    }
  }
}
```

**Expected** **`metric_score`** near 0 when Moby Dick (`2701`) is rated irrelevant. Change **`"rating": 0`** to **`4`** and re-run to see the score improve.

**Fast mode**  
`02-rank-eval.bru`


### **Step 3: Teaching search pipeline (script_score)**

**Why**  
Demonstrates **`request_processors`** that wrap every query. This version is **deliberately flawed** — `"query": "in_stock: true"` is a string, not a real filter. Lesson script **`05-full-bookstore-pipeline.py`** shows the corrected pattern.

**Request** — paste into Dev Tools:

```http
PUT _search/pipeline/bookstore-score-filter
{
  "description": "Change scores on books based on ratings and publish date from search results",
  "request_processors": [
    {
      "filter_query": {
        "query": {
          "script_score": {
            "query": "in_stock: true",
            "script": {
              "source": "(doc['publish_date'].value - 2020)* 0.5 + doc['ratings'].value * 0.1"
            }
          }
        }
      }
    }
  ]
}
```

**Fast mode**  
`03-create-score-filter-pipeline.bru`


### **Step 4: Set default search pipeline on the index**

**Why**  
**`index.search.default_pipeline`** applies the pipeline to every search automatically (distinct from **`index.default_pipeline`**, which is ingest).

**Note:** The reference script sets **`bookstore-stock-filter`**. Ensure that pipeline exists (or substitute a pipeline id you created earlier). To bypass a default for one request, use **`?search_pipeline=_none`**.

**Request** — paste into Dev Tools:

```http
PUT bookstore-rag/_settings
{
  "index.search.default_pipeline": "bookstore-stock-filter"
}
```

**Fast mode**  
`04-set-default-search-pipeline.bru`


### **Step 5: Production-style full bookstore pipeline**

**Why**  
Combines a real **`term`** filter on **`in_stock`** with the same **min_max** normalization used in hybrid search — business rules + relevance in one place.

**Request** — paste into Dev Tools:

```http
PUT _search/pipeline/bookstore-full-pipeline
{
  "description": "Full bookstore search pipeline",
  "request_processors": [
    {
      "filter_query": {
        "query": {
          "term": {
            "in_stock": true
          }
        },
        "tag": "stock_filter"
      }
    }
  ],
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

Use it explicitly on hybrid queries:

**Request** — paste into Dev Tools:


```http
GET bookstore-rag/_search?search_pipeline=bookstore-full-pipeline
{
  "query": {
    "hybrid": {
      "queries": [
        { "match": { "content": { "query": "whale" } } },
        {
          "knn": {
            "content_embedding": {
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
`05-create-full-pipeline.bru` → `06-hybrid-with-full-pipeline.bru`

---

## What you learned

- **`explain`** for score debugging; **`_rank_eval`** for measurable relevance
- **`request_processors`** vs **`phase_results_processors`** in search pipelines
- How to enforce **in-stock** filtering without changing application query code

## Next chapter

[Chapter 5 · Lesson 1](../../Chapter%205/Lesson%201/README.md) — production cluster operations (routing, shards, watermarks).

## Theory-only follow-up

**Chapter 4 · Lesson 4 (theory only)** — OpenSearch MCP server — see [lessons without a lab folder](../../../HANDS-ON-GUIDE.md#lessons-without-a-lab-folder).

## Reference scripts

| Script | Same as |
|--------|---------|
| `01-explain-hybrid-search.py` | Step 1 |
| `02-rank-eval.py` | Step 2 |
| `03-in-stock-pipeline.py` | Step 3 |
| `04-add-stock-filter.py` | Step 4 |
| `05-full-bookstore-pipeline.py` | Step 5 |

```bash
python 01-explain-hybrid-search.py
python 02-rank-eval.py
python 03-in-stock-pipeline.py
python 04-add-stock-filter.py
python 05-full-bookstore-pipeline.py
```
