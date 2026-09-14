---
source_id: "DOC-00859"
title: "Troubleshooting dataset lineage"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > Troubleshooting dataset lineage"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2024-07-26"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# Troubleshooting dataset lineage

This page explains how dataset lineage works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, dataset lineage is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When dataset lineage is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
