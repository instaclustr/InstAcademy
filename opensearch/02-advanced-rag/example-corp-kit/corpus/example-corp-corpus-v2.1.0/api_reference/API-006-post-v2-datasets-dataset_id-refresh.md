---
source_id: "API-006"
title: "POST /v2/datasets/{dataset_id}/refresh"
doc_type: "api-reference"
section_path: "API Reference > Trigger a dataset refresh"
method: "POST"
path: "/v2/datasets/{dataset_id}/refresh"
related_error_codes: ["ERR-3305", "ERR-6601"]
acl: "public"
updated_at: "2026-06-30"
---

# POST /v2/datasets/{dataset_id}/refresh

Trigger a dataset refresh.

All endpoints require a service account bearer token in the Authorization header. Rate limit: 600 requests per minute per service account. Exceeding it returns HTTP 429 with error code ERR-6601.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| dataset_id | string | Yes |
| mode | string | No |

## Errors

- ERR-3305
- ERR-6601

## Example

```bash
curl -X POST \
  'https://api.example-corp.com/v2/datasets/{dataset_id}/refresh' \
  -H 'Authorization: Bearer $TOKEN'
```