---
source_id: "API-008"
title: "GET /v2/connectors"
doc_type: "api-reference"
section_path: "API Reference > List connectors"
method: "GET"
path: "/v2/connectors"
related_error_codes: ["ERR-6601"]
acl: "public"
updated_at: "2026-06-30"
---

# GET /v2/connectors

List connectors.

All endpoints require a service account bearer token in the Authorization header. Rate limit: 600 requests per minute per service account. Exceeding it returns HTTP 429 with error code ERR-6601.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| workspace_id | string | Yes |

## Errors

- ERR-6601

## Example

```bash
curl -X GET \
  'https://api.example-corp.com/v2/connectors' \
  -H 'Authorization: Bearer $TOKEN'
```