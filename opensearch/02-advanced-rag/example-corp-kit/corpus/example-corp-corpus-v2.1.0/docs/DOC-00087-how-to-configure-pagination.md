---
source_id: "DOC-00087"
title: "How to configure pagination"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > How to configure pagination"
product_area: "api"
product_version: "5.1"
acl: "enterprise"
updated_at: "2024-10-27"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# How to configure pagination

Pagination is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When pagination is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for pagination are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: pagination performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, pagination is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
