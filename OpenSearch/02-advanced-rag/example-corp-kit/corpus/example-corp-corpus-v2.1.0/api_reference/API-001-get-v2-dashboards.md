---
source_id: "API-001"
title: "GET /v2/dashboards"
doc_type: "api-reference"
section_path: "API Reference > List dashboards"
method: "GET"
path: "/v2/dashboards"
related_error_codes: ["ERR-6601"]
acl: "public"
updated_at: "2026-06-30"
---

# GET /v2/dashboards

List dashboards.

All endpoints require a service account bearer token in the Authorization header. Rate limit: 600 requests per minute per service account. Exceeding it returns HTTP 429 with error code ERR-6601.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| workspace_id | string | Yes |
| page | integer | No |
| page_size | integer | No |

## Errors

- ERR-6601

## Example

```bash
curl -X GET \
  'https://api.example-corp.com/v2/dashboards' \
  -H 'Authorization: Bearer $TOKEN'
```