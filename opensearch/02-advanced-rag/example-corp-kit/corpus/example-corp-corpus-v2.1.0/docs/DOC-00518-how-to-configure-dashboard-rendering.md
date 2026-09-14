---
source_id: "DOC-00518"
title: "How to configure dashboard rendering"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > How to configure dashboard rendering"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2024-07-12"
related_error_codes: ["ERR-1210"]
---

# How to configure dashboard rendering

Dashboard Rendering is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, dashboard rendering is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable dashboard rendering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
