---
source_id: "DOC-00054"
title: "How to configure mobile layouts"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > How to configure mobile layouts"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2025-03-05"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# How to configure mobile layouts

Mobile Layouts is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for mobile layouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, mobile layouts is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, mobile layouts inherits group membership from your identity provider on each login.

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
