---
source_id: "DOC-00759"
title: "How to configure mobile layouts"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > How to configure mobile layouts"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2024-09-26"
related_error_codes: ["ERR-1210", "ERR-1147"]
---

# How to configure mobile layouts

Mobile Layouts is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, mobile layouts is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, mobile layouts inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
