---
source_id: "API-011"
title: "POST /v2/webhooks"
doc_type: "api-reference"
section_path: "API Reference > Register a webhook"
method: "POST"
path: "/v2/webhooks"
related_error_codes: ["ERR-4415", "ERR-6601"]
acl: "public"
updated_at: "2026-06-30"
---

# POST /v2/webhooks

Register a webhook.

All endpoints require a service account bearer token in the Authorization header. Rate limit: 600 requests per minute per service account. Exceeding it returns HTTP 429 with error code ERR-6601.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| url | string | Yes |
| events | array | Yes |
| secret | string | No |

## Errors

- ERR-4415
- ERR-6601

## Example

```bash
curl -X POST \
  'https://api.example-corp.com/v2/webhooks' \
  -H 'Authorization: Bearer $TOKEN'
```