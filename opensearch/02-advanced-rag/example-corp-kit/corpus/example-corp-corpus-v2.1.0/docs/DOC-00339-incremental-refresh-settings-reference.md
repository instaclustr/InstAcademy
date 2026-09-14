---
source_id: "DOC-00339"
title: "Incremental Refresh settings reference"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > Incremental Refresh settings reference"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2025-05-08"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# Incremental Refresh settings reference

Incremental Refresh lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, incremental refresh is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: incremental refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable incremental refresh, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for incremental refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
