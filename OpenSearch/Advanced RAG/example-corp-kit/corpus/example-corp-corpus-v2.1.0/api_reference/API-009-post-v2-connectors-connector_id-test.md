---
source_id: "API-009"
title: "POST /v2/connectors/{connector_id}/test"
doc_type: "api-reference"
section_path: "API Reference > Test a connector"
method: "POST"
path: "/v2/connectors/{connector_id}/test"
related_error_codes: ["ERR-2209", "ERR-2231", "ERR-2288"]
acl: "public"
updated_at: "2026-06-30"
---

# POST /v2/connectors/{connector_id}/test

Test a connector.

All endpoints require a service account bearer token in the Authorization header. Rate limit: 600 requests per minute per service account. Exceeding it returns HTTP 429 with error code ERR-6601.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| connector_id | string | Yes |

## Errors

- ERR-2209
- ERR-2231
- ERR-2288

## Example

```bash
curl -X POST \
  'https://api.example-corp.com/v2/connectors/{connector_id}/test' \
  -H 'Authorization: Bearer $TOKEN'
```