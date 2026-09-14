---
source_id: "API-014"
title: "GET /v2/queries/{query_id}/results"
doc_type: "api-reference"
section_path: "API Reference > Fetch SQL Workbench results"
method: "GET"
path: "/v2/queries/{query_id}/results"
related_error_codes: ["ERR-5501", "ERR-6601"]
acl: "public"
updated_at: "2026-06-30"
---

# GET /v2/queries/{query_id}/results

Fetch SQL Workbench results.

All endpoints require a service account bearer token in the Authorization header. Rate limit: 600 requests per minute per service account. Exceeding it returns HTTP 429 with error code ERR-6601.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| query_id | string | Yes |
| cursor | string | No |

## Errors

- ERR-5501
- ERR-6601

## Example

```bash
curl -X GET \
  'https://api.example-corp.com/v2/queries/{query_id}/results' \
  -H 'Authorization: Bearer $TOKEN'
```