---
source_id: "DOC-00289"
title: "How to configure mobile layouts"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > How to configure mobile layouts"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2025-10-14"
related_error_codes: ["ERR-1210"]
---

# How to configure mobile layouts

This page explains how mobile layouts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, mobile layouts is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for mobile layouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
