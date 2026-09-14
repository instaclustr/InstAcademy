---
source_id: "DOC-00061"
title: "How to configure materialized views"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > How to configure materialized views"
product_area: "datasets"
product_version: "5.0"
acl: "standard"
updated_at: "2024-02-16"
related_error_codes: ["ERR-3305"]
---

# How to configure materialized views

This page explains how materialized views works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, materialized views is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
