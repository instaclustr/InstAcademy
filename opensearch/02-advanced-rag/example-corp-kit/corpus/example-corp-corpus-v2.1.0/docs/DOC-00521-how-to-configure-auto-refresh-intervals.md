---
source_id: "DOC-00521"
title: "How to configure auto-refresh intervals"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > How to configure auto-refresh intervals"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-03-19"
related_error_codes: ["ERR-1210"]
---

# How to configure auto-refresh intervals

Auto-Refresh Intervals is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

By default, auto-refresh intervals is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
