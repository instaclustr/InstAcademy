---
source_id: "API-012"
title: "GET /v2/audit/events"
doc_type: "api-reference"
section_path: "API Reference > Query audit events"
method: "GET"
path: "/v2/audit/events"
related_error_codes: ["ERR-6601"]
acl: "public"
updated_at: "2026-06-30"
---

# GET /v2/audit/events

Query audit events.

All endpoints require a service account bearer token in the Authorization header. Rate limit: 600 requests per minute per service account. Exceeding it returns HTTP 429 with error code ERR-6601.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| from | string | Yes |
| to | string | Yes |
| actor | string | No |

## Errors

- ERR-6601

## Example

```bash
curl -X GET \
  'https://api.example-corp.com/v2/audit/events' \
  -H 'Authorization: Bearer $TOKEN'
```