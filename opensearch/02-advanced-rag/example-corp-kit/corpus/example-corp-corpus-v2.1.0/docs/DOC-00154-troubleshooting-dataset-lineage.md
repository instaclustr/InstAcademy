---
source_id: "DOC-00154"
title: "Troubleshooting dataset lineage"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > Troubleshooting dataset lineage"
product_area: "datasets"
product_version: "4.8"
acl: "enterprise"
updated_at: "2026-01-27"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# Troubleshooting dataset lineage

Dataset Lineage lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

When dataset lineage is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
