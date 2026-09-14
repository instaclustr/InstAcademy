---
source_id: "DOC-00810"
title: "Calculated Fields settings reference"
doc_type: "product-docs"
section_path: "Datasets > Calculated Fields > Calculated Fields settings reference"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2025-08-03"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# Calculated Fields settings reference

This page explains how calculated fields works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for calculated fields are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, calculated fields is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: calculated fields performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When calculated fields is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable calculated fields, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
