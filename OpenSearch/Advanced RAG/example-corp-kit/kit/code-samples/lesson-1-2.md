# Lesson 1.2 code samples: Building the RAG Pipeline

## Hybrid query: both retrieval legs in one request

The support tool question "Snowflake connector failing with ERR-2209"
carries an exact term (the code) and a described symptom. Run both legs.

```json
GET support-docs/_search?search_pipeline=support-hybrid-rrf
{
  "size": 10,
  "query": {
    "hybrid": {
      "queries": [
        { "match": { "text": "Snowflake connector failing ERR-2209" } },
        {
          "neural": {
            "embedding": {
              "query_text": "Snowflake connector failing with ERR-2209",
              "model_id": "<MODEL_ID>",
              "k": 50
            }
          }
        }
      ]
    }
  }
}
```

## Search pipeline A: RRF (rank based, robust default)

```json
PUT _search/pipeline/support-hybrid-rrf
{
  "description": "Hybrid merge via reciprocal rank fusion",
  "phase_results_processors": [
    {
      "score-ranker-processor": {
        "combination": {
          "technique": "rrf",
          "rank_constant": 60
        }
      }
    }
  ]
}
```

## Search pipeline B: normalized weighted fusion (explicit control)

```json
PUT _search/pipeline/support-hybrid-weighted
{
  "description": "min_max normalization, 40% lexical / 60% semantic",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": { "technique": "min_max" },
        "combination": {
          "technique": "arithmetic_mean",
          "parameters": { "weights": [0.4, 0.6] }
        }
      }
    }
  ]
}
```

Compare the two on camera with the eval harness:

```bash
python3 scripts/eval_retrieval.py --mode hybrid --k 5 --kb-only \
  --model-id <MODEL_ID> --search-pipeline support-hybrid-rrf \
  --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
python3 scripts/eval_retrieval.py --mode hybrid --k 5 --kb-only \
  --model-id <MODEL_ID> --search-pipeline support-hybrid-weighted \
  --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
```

## Pre-filter: hard constraints inside the candidate set

Tenant ACL and product version are non-negotiable. A standard-tier
customer on 4.9 must never retrieve enterprise-only content, and 5.1
docs can mislead them. Filters ride inside each leg.

```json
GET support-docs/_search?search_pipeline=support-hybrid-rrf
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "bool": {
            "must": { "match": { "text": "schema discovery timed out" } },
            "filter": [
              { "terms": { "acl": ["public", "standard"] } },
              { "term": { "product_version": "4.9" } }
            ]
          }
        },
        {
          "neural": {
            "embedding": {
              "query_text": "schema discovery timed out",
              "model_id": "<MODEL_ID>",
              "k": 50,
              "filter": {
                "bool": {
                  "filter": [
                    { "terms": { "acl": ["public", "standard"] } },
                    { "term": { "product_version": "4.9" } }
                  ]
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

## Reranking a shortlist (rerank processor)

Wide recall, fuse, then spend heavy compute on the top N only.

```json
PUT _search/pipeline/support-hybrid-rrf-rerank
{
  "phase_results_processors": [
    { "score-ranker-processor": {
        "combination": { "technique": "rrf", "rank_constant": 60 } } }
  ],
  "response_processors": [
    {
      "rerank": {
        "ml_opensearch": { "model_id": "<CROSS_ENCODER_MODEL_ID>" },
        "context": { "document_fields": ["text"] }
      }
    }
  ]
}
```

## Stage instrumentation: log the funnel per request

Candidates per leg, post-fusion, into rerank, post-filter. Four numbers
tell you which stage broke before you touch a single knob.
