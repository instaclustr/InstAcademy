# Lesson 1.1 code samples: OpenSearch as a RAG Engine

All samples run against the Example Corp corpus (`support-docs` alias)
created by `scripts/ingest_chunks.py`. OpenSearch 3.6+.

## BM25: exact-term retrieval (error codes)

A customer pastes an error code. Lexical search nails it.

```json
GET support-docs/_search
{
  "query": {
    "match": { "text": "ERR-2209" }
  },
  "_source": ["title", "section_heading", "doc_type"]
}
```

## knn_vector mapping (Faiss HNSW, the 3.x default engine)

NMSLIB is deprecated and new NMSLIB indexes are blocked since 3.0.
Define engine and parameters explicitly; never rely on defaults in prod.

```json
PUT support-docs-v1
{
  "settings": { "index": { "knn": true } },
  "mappings": {
    "properties": {
      "text": { "type": "text" },
      "embedding": {
        "type": "knn_vector",
        "dimension": 384,
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "space_type": "innerproduct",
          "parameters": { "m": 16, "ef_construction": 128 }
        }
      }
    }
  }
}
```

## Neural query: semantic retrieval (symptom language)

The customer says "dashboard takes forever to load." No doc uses those
words, but the render performance page is semantically close.

```json
GET support-docs/_search
{
  "query": {
    "neural": {
      "embedding": {
        "query_text": "dashboard takes forever to load",
        "model_id": "<MODEL_ID>",
        "k": 50
      }
    }
  }
}
```

## ef_search: the query-time recall/latency dial

```json
PUT support-docs-v1/_settings
{
  "index": { "knn.algo_param.ef_search": 100 }
}
```

Tune against the golden set, not intuition:

```bash
python3 scripts/eval_retrieval.py --mode neural --k 5 --model-id <MODEL_ID> --kb-only \
  --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
```

## Semantic field type: the convenience layer (3.1+)

One field, no manual ingest pipeline. You still choose the model and
the chunking; the field only automates embedding generation.

```json
PUT support-quickstart
{
  "mappings": {
    "properties": {
      "text": {
        "type": "semantic",
        "model_id": "<MODEL_ID>"
      }
    }
  }
}
```

## 3.6 note: quantization headroom

If memory becomes the constraint at Example Corp scale, evaluate
quantization before scaling hardware. OpenSearch supports fp16, int8,
int4, and binary vector formats, and 3.6 adds Lucene BBQ with up to 32x
compression.
