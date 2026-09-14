---
source_id: "DOC-00098"
title: "Auto-Refresh Intervals settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > Auto-Refresh Intervals settings reference"
product_area: "dashboards"
product_version: "5.1"
acl: "enterprise"
updated_at: "2026-03-03"
related_error_codes: ["ERR-1210"]
---

# Auto-Refresh Intervals settings reference

Auto-Refresh Intervals lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, auto-refresh intervals is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
