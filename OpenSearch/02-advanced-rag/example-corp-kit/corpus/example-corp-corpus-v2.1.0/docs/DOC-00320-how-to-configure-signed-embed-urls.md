---
source_id: "DOC-00320"
title: "How to configure signed embed URLs"
doc_type: "product-docs"
section_path: "REST API & Embedding > Signed Embed Urls > How to configure signed embed URLs"
product_area: "api"
product_version: "5.1"
acl: "professional"
updated_at: "2025-06-20"
related_error_codes: ["ERR-6640"]
---

# How to configure signed embed URLs

Signed Embed Urls lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, signed embed URLs inherits group membership from your identity provider on each login.

To enable signed embed URLs, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, signed embed URLs is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: signed embed URLs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When signed embed URLs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
