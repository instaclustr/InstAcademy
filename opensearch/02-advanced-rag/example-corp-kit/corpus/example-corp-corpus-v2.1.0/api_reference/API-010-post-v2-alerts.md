---
source_id: "API-010"
title: "POST /v2/alerts"
doc_type: "api-reference"
section_path: "API Reference > Create an alert"
method: "POST"
path: "/v2/alerts"
related_error_codes: ["ERR-4402", "ERR-6601"]
acl: "public"
updated_at: "2026-06-30"
---

# POST /v2/alerts

Create an alert.

All endpoints require a service account bearer token in the Authorization header. Rate limit: 600 requests per minute per service account. Exceeding it returns HTTP 429 with error code ERR-6601.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| dashboard_id | string | Yes |
| condition | object | Yes |
| channels | array | Yes |

## Errors

- ERR-4402
- ERR-6601

## Example

```bash
curl -X POST \
  'https://api.example-corp.com/v2/alerts' \
  -H 'Authorization: Bearer $TOKEN'
```