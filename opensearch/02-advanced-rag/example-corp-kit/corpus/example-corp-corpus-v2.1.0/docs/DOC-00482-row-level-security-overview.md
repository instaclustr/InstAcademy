---
source_id: "DOC-00482"
title: "Row-Level Security overview"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > Row-Level Security overview"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2026-06-14"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# Row-Level Security overview

This page explains how row-level security works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, row-level security is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
