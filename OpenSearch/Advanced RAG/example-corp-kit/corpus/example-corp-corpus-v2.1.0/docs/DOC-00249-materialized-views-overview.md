---
source_id: "DOC-00249"
title: "Materialized Views overview"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > Materialized Views overview"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2026-04-30"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# Materialized Views overview

Materialized Views lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, materialized views is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
