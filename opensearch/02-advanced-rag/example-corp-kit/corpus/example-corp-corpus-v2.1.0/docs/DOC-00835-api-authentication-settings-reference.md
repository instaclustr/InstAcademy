---
source_id: "DOC-00835"
title: "Api Authentication settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > Api Authentication settings reference"
product_area: "api"
product_version: "5.0"
acl: "public"
updated_at: "2026-01-12"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# Api Authentication settings reference

Api Authentication is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable API authentication, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, API authentication is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: API authentication performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, API authentication inherits group membership from your identity provider on each login.

Audit events for API authentication are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
