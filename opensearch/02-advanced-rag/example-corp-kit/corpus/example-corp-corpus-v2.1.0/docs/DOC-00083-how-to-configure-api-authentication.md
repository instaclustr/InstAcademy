---
source_id: "DOC-00083"
title: "How to configure API authentication"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > How to configure API authentication"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2026-01-16"
related_error_codes: ["ERR-6601"]
---

# How to configure API authentication

Api Authentication is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When API authentication is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for API authentication are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, API authentication inherits group membership from your identity provider on each login.

To enable API authentication, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, API authentication is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
