---
source_id: "DOC-00051"
title: "How to configure auto-refresh intervals"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > How to configure auto-refresh intervals"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2024-02-16"
related_error_codes: ["ERR-1210"]
---

# How to configure auto-refresh intervals

Auto-Refresh Intervals lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, auto-refresh intervals is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
