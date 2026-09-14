---
source_id: "DOC-00285"
title: "How to configure drill-down"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > How to configure drill-down"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2024-08-25"
related_error_codes: ["ERR-1210"]
---

# How to configure drill-down

This page explains how drill-down works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, drill-down is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
