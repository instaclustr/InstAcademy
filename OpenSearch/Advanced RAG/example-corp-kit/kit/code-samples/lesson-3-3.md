# Lesson 3.3 code samples: Evaluation & Observability

## The traces index (OpenSearch as the observability layer)

```json
PUT support-traces
{
  "mappings": {
    "properties": {
      "request_id":        { "type": "keyword" },
      "created_at":        { "type": "date" },
      "tenant_id":         { "type": "keyword" },
      "product_area":      { "type": "keyword" },
      "customer_version":  { "type": "keyword" },
      "query":             { "type": "text" },
      "rewritten_query":   { "type": "text" },
      "enhancement":       { "type": "keyword" },
      "retrieved_chunk_ids": { "type": "keyword" },
      "top_score":         { "type": "float" },
      "score_shape":       { "type": "keyword" },
      "grader_verdicts":   { "type": "object", "enabled": false },
      "retries":           { "type": "integer" },
      "confidence":        { "type": "keyword" },
      "context_relevance": { "type": "float" },
      "faithfulness":      { "type": "float" },
      "answer_correctness":{ "type": "float" },
      "latency_ms":        { "type": "object",
        "properties": {
          "retrieval": { "type": "integer" },
          "grading":   { "type": "integer" },
          "generation":{ "type": "integer" },
          "total":     { "type": "integer" }
        }}
    }
  }
}
```

## The dashboard questions become queries

Faithfulness by product area this week:

```json
GET support-traces/_search
{
  "size": 0,
  "query": { "range": { "created_at": { "gte": "now-7d" } } },
  "aggs": {
    "by_area": {
      "terms": { "field": "product_area" },
      "aggs": { "avg_faithfulness": { "avg": { "field": "faithfulness" } } }
    }
  }
}
```

Did correction help, or just add latency?

```json
GET support-traces/_search
{
  "size": 0,
  "aggs": {
    "by_retries": {
      "terms": { "field": "retries" },
      "aggs": {
        "faithfulness": { "avg": { "field": "faithfulness" } },
        "p95_latency": { "percentiles":
          { "field": "latency_ms.total", "percents": [95] } }
      }
    }
  }
}
```

## RAGAS: LLM-as-judge on the support tool answer stream

```python
# pip install ragas datasets
from ragas import evaluate
from ragas.metrics import faithfulness, context_precision, answer_correctness
from datasets import Dataset

rows = Dataset.from_dict({
    "question":     [t["query"] for t in traces],
    "contexts":     [t["chunk_texts"] for t in traces],
    "answer":       [t["answer"] for t in traces],
    # resolved tickets = free reference answers
    "ground_truth": [t["ticket_resolution"] for t in traces],
})
scores = evaluate(rows, metrics=[faithfulness, context_precision,
                                 answer_correctness])
# write scores back onto the trace documents
```

Calibrate before trusting: sample ~50 answers, have support leads score
them, and check agreement with the judge. An uncalibrated judge is a
dashboard that lies with confidence.

## User feedback as labels (via the Memory API message update)

Agents accept or edit every draft. Log the outcome onto the message and
feed it back to the golden set:

```json
PUT /_plugins/_ml/memory/message/<MESSAGE_ID>
{
  "additional_info": {
    "feedback": "edited",
    "agent_diff": "replaced 5.0 instructions with 4.9 workaround",
    "label": "negative_version_fit"
  }
}
```

```python
# nightly: harvest labels into golden_set.jsonl
# accept -> positive label for the retrieved chunk_ids
# edit   -> correction pair (query, wrong chunks, right chunks)
# reject -> hard negative
```
