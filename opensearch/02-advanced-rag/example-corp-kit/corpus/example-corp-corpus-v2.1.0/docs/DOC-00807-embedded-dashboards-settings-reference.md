---
source_id: "DOC-00807"
title: "Embedded Dashboards settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > Embedded Dashboards settings reference"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2025-09-13"
related_error_codes: ["ERR-1102", "ERR-1210"]
---

# Embedded Dashboards settings reference

Embedded Dashboards lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

By default, embedded dashboards is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for embedded dashboards are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
