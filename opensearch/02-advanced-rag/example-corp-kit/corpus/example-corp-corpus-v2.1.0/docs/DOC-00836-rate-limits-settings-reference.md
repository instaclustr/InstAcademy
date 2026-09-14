---
source_id: "DOC-00836"
title: "Rate Limits settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > Rate Limits settings reference"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2026-04-06"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# Rate Limits settings reference

Rate Limits lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, rate limits inherits group membership from your identity provider on each login.

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
