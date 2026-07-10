---
source_id: "DOC-00790"
title: "How to configure signed embed URLs"
doc_type: "product-docs"
section_path: "REST API & Embedding > Signed Embed Urls > How to configure signed embed URLs"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2025-01-06"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# How to configure signed embed URLs

Signed Embed Urls is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When signed embed URLs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable signed embed URLs, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, signed embed URLs inherits group membership from your identity provider on each login.

Performance tip: signed embed URLs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for signed embed URLs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
