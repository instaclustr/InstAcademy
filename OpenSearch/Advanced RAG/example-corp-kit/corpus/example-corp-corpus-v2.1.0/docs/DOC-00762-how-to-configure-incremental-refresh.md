---
source_id: "DOC-00762"
title: "How to configure incremental refresh"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > How to configure incremental refresh"
product_area: "datasets"
product_version: "5.0"
acl: "professional"
updated_at: "2025-10-31"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# How to configure incremental refresh

Incremental Refresh lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for incremental refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, incremental refresh is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable incremental refresh, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: incremental refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
