---
source_id: "API-004"
title: "POST /v2/embed/urls"
doc_type: "api-reference"
section_path: "API Reference > Create a signed embed URL"
method: "POST"
path: "/v2/embed/urls"
related_error_codes: ["ERR-6640", "ERR-6601"]
acl: "public"
updated_at: "2026-06-30"
---

# POST /v2/embed/urls

Create a signed embed URL.

All endpoints require a service account bearer token in the Authorization header. Rate limit: 600 requests per minute per service account. Exceeding it returns HTTP 429 with error code ERR-6601.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| dashboard_id | string | Yes |
| user_attributes | object | No |
| expires_in | integer | No |

## Errors

- ERR-6640
- ERR-6601

## Example

```bash
curl -X POST \
  'https://api.example-corp.com/v2/embed/urls' \
  -H 'Authorization: Bearer $TOKEN'
```