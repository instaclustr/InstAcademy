---
source_id: "DOC-00130"
title: "Api Authentication settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > Api Authentication settings reference"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2026-03-20"
related_error_codes: ["ERR-6640"]
---

# Api Authentication settings reference

Api Authentication lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, API authentication inherits group membership from your identity provider on each login.

Performance tip: API authentication performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When API authentication is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, API authentication is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for API authentication are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
