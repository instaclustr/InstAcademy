---
source_id: "API-013"
title: "POST /v2/scim/Users"
doc_type: "api-reference"
section_path: "API Reference > Provision a user (SCIM)"
method: "POST"
path: "/v2/scim/Users"
related_error_codes: ["ERR-7733"]
acl: "public"
updated_at: "2026-06-30"
---

# POST /v2/scim/Users

Provision a user (SCIM).

All endpoints require a service account bearer token in the Authorization header. Rate limit: 600 requests per minute per service account. Exceeding it returns HTTP 429 with error code ERR-6601.

## Parameters

| Name | Type | Required |
| --- | --- | --- |
| userName | string | Yes |
| emails | array | Yes |

## Errors

- ERR-7733

## Example

```bash
curl -X POST \
  'https://api.example-corp.com/v2/scim/Users' \
  -H 'Authorization: Bearer $TOKEN'
```