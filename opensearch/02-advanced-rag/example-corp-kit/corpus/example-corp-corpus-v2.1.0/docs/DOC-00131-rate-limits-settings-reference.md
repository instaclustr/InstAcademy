---
source_id: "DOC-00131"
title: "Rate Limits settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > Rate Limits settings reference"
product_area: "api"
product_version: "5.0"
acl: "public"
updated_at: "2024-09-07"
related_error_codes: ["ERR-6640"]
---

# Rate Limits settings reference

Rate Limits lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, rate limits is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, rate limits inherits group membership from your identity provider on each login.

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
