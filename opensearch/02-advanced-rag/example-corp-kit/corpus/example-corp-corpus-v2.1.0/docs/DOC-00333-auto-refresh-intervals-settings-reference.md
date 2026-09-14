---
source_id: "DOC-00333"
title: "Auto-Refresh Intervals settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > Auto-Refresh Intervals settings reference"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2025-04-23"
related_error_codes: ["ERR-1210", "ERR-1147"]
---

# Auto-Refresh Intervals settings reference

Auto-Refresh Intervals lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

By default, auto-refresh intervals is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
