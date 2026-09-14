---
source_id: "DOC-00755"
title: "How to configure drill-down"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > How to configure drill-down"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2024-06-26"
related_error_codes: ["ERR-1147"]
---

# How to configure drill-down

Drill-Down is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for drill-down are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, drill-down is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
