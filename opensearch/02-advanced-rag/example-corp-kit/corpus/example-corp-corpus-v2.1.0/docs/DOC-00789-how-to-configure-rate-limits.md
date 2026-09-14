---
source_id: "DOC-00789"
title: "How to configure rate limits"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > How to configure rate limits"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2025-02-26"
related_error_codes: ["ERR-6601"]
---

# How to configure rate limits

Rate Limits lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, rate limits inherits group membership from your identity provider on each login.

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, rate limits is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
