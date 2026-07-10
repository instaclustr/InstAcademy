# Lesson 1.4 code samples: Connectors, Ingest Patterns & Updates

## ML Commons connector to an external embedding endpoint

Credentials live in the connector, never in application code or logs.
One connector per environment, least privilege, one host, one model.

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "support-embeddings-prod",
  "description": "Embedding endpoint for the support tool, prod only",
  "version": 1,
  "protocol": "http",
  "credential": {
    "api_key": "<STORED_ENCRYPTED_BY_ML_COMMONS>"
  },
  "parameters": {
    "endpoint": "api.embeddings-provider.com",
    "model": "text-embed-v3-small"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://${parameters.endpoint}/v1/embeddings",
      "headers": {
        "Authorization": "Bearer ${credential.api_key}"
      },
      "request_body": "{ \"input\": ${parameters.input}, \"model\": \"${parameters.model}\" }"
    }
  ]
}
```

## Model group lifecycle

```json
POST /_plugins/_ml/model_groups/_register
{
  "name": "support-embedding-models",
  "description": "Embedding models for the support tool knowledge base"
}
```

```json
POST /_plugins/_ml/models/_register
{
  "name": "support-embedding-remote",
  "version": "2.0.0",
  "model_group_id": "<MODEL_GROUP_ID>",
  "function_name": "remote",
  "connector_id": "<CONNECTOR_ID>"
}
```

```json
POST /_plugins/_ml/models/<MODEL_ID>/_deploy
```

Validate on a sample before cutover: dimensions match the mapping,
latency is acceptable, error rate is near zero. Then cut over ingest
and search together, reindex, and only undeploy v1 when nothing
references it. Every chunk stores `embedding_model_id` and
`embedding_model_version` so mixed-vector indexes are detectable.

Flow Framework can capture this entire setup (connector, model group,
model, ingest pipeline, index) as a single declarative template, so
dev, stage, and prod are provisioned from code instead of console clicks.

## Bulk sizing with backpressure

See `bulk_load()` in `scripts/ingest_chunks.py`: modest batches,
watch for 429 rejections, halve the batch and back off instead of
retry-storming. Fail loudly if any doc indexes without an embedding.

```bash
export OS_URL=https://user:pass@your-cluster:9200
python3 scripts/ingest_chunks.py --model-id <MODEL_ID> \
  --chunks corpus/example-corp-corpus-v2.1.0/chunks.jsonl --batch-size 200
```

Bootstrap trick for the initial 200k-ticket load: relax refresh during
the load, restore it after.

```json
PUT support-docs-v1/_settings
{ "index": { "refresh_interval": "-1" } }
```

```json
PUT support-docs-v1/_settings
{ "index": { "refresh_interval": "1s" } }
```

## Update patterns for the support tool assets

| Asset | Pattern | Why |
| --- | --- | --- |
| Product docs | Scheduled nightly, watermark on `updated_at` | Docs publish in batches |
| Integration guides | Scheduled weekly | Slow moving |
| Known issues | Event-driven | Every new issue must be searchable immediately |
| Resolved tickets | Streaming via Kafka | Hundreds close per day; partition by ticket_id, idempotent writes |

Watermark query for the nightly docs sync:

```json
GET docs-source/_search
{
  "query": { "range": { "updated_at": { "gt": "<LAST_SYNC_TIMESTAMP>" } } }
}
```

Plus one scheduled reconciliation job to fix drift, because deletes and
dropped events happen. Alias flip for zero-downtime reindex:

```json
POST /_aliases
{
  "actions": [
    { "remove": { "index": "support-docs-v1", "alias": "support-docs" } },
    { "add":    { "index": "support-docs-v2", "alias": "support-docs" } }
  ]
}
```
