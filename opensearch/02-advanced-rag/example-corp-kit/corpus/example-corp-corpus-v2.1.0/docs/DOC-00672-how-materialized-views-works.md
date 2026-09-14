---
source_id: "DOC-00672"
title: "How materialized views works"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > How materialized views works"
product_area: "datasets"
product_version: "4.9"
acl: "professional"
updated_at: "2025-02-15"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# How materialized views works

This page explains how materialized views works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, materialized views is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
