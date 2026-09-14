---
source_id: "DOC-00368"
title: "Webhook Signatures settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > Webhook Signatures settings reference"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2026-05-08"
related_error_codes: ["ERR-6601"]
---

# Webhook Signatures settings reference

Webhook Signatures lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, webhook signatures is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
