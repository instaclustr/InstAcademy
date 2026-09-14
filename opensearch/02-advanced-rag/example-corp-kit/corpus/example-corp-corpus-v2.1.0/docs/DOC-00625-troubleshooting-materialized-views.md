---
source_id: "DOC-00625"
title: "Troubleshooting materialized views"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > Troubleshooting materialized views"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2024-06-02"
related_error_codes: ["ERR-3340"]
---

# Troubleshooting materialized views

This page explains how materialized views works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, materialized views is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
