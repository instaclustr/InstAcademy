---
source_id: "API-003"
title: "POST /v2/dashboards/{dashboard_id}/export"
doc_type: "api-reference"
section_path: "API Reference > Export a dashboard to PDF"
method: "POST"
path: "/v2/dashboards/{dashboard_id}/export"
related_error_codes: ["ERR-1210", "ERR-6601"]
acl: "public"
updated_at: "2026-06-30"
---

# POST /v2/dashboards/{dashboard_id}/export

Export a dashboard to PDF.

All endpoints require a service account bearer token in the Authorization header. Rate limit: 600 requests per minute per service account. Exceeding it returns HTTP 429 with error code ERR-6601.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| dashboard_id | string | Yes |
| format | string | No |
| dpi | integer | No |

## Errors

- ERR-1210
- ERR-6601

## Example

```bash
curl -X POST \
  'https://api.example-corp.com/v2/dashboards/{dashboard_id}/export' \
  -H 'Authorization: Bearer $TOKEN'
```