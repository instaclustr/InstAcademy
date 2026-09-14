---
source_id: "DOC-00673"
title: "How refresh failure retries works"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > How refresh failure retries works"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2024-07-02"
related_error_codes: ["ERR-3305"]
---

# How refresh failure retries works

This page explains how refresh failure retries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, refresh failure retries is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When refresh failure retries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
