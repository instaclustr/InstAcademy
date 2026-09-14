---
source_id: "DOC-00432"
title: "How dataset refresh scheduling works"
doc_type: "product-docs"
section_path: "Datasets > Dataset Refresh Scheduling > How dataset refresh scheduling works"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2025-10-19"
related_error_codes: ["ERR-3305"]
---

# How dataset refresh scheduling works

Dataset Refresh Scheduling lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

When dataset refresh scheduling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for dataset refresh scheduling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: dataset refresh scheduling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable dataset refresh scheduling, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, dataset refresh scheduling is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
