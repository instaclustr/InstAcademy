---
source_id: "DOC-00812"
title: "Dataset Lineage settings reference"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > Dataset Lineage settings reference"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2026-05-01"
related_error_codes: ["ERR-3305"]
---

# Dataset Lineage settings reference

Dataset Lineage is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, dataset lineage is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When dataset lineage is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
