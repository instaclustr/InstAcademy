---
source_id: "DOC-00806"
title: "Mobile Layouts settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > Mobile Layouts settings reference"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-09-03"
related_error_codes: ["ERR-1210"]
---

# Mobile Layouts settings reference

Mobile Layouts lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, mobile layouts is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, mobile layouts inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
