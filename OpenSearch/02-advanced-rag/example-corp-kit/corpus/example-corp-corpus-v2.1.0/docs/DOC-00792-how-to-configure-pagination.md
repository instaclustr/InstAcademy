---
source_id: "DOC-00792"
title: "How to configure pagination"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > How to configure pagination"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2024-05-04"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# How to configure pagination

Pagination lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

Audit events for pagination are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, pagination inherits group membership from your identity provider on each login.

When pagination is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: pagination performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
