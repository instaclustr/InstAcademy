---
source_id: "DOC-00319"
title: "How to configure rate limits"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > How to configure rate limits"
product_area: "api"
product_version: "5.0"
acl: "public"
updated_at: "2026-06-01"
related_error_codes: ["ERR-6601"]
---

# How to configure rate limits

Rate Limits lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, rate limits inherits group membership from your identity provider on each login.

By default, rate limits is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
