---
source_id: "DOC-00553"
title: "How to configure API authentication"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > How to configure API authentication"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2024-08-28"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# How to configure API authentication

Api Authentication lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

When API authentication is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable API authentication, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for API authentication are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: API authentication performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, API authentication is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
