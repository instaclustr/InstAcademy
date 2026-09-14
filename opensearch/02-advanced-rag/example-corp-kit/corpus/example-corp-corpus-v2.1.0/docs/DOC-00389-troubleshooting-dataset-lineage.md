---
source_id: "DOC-00389"
title: "Troubleshooting dataset lineage"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > Troubleshooting dataset lineage"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2026-03-22"
related_error_codes: ["ERR-3340"]
---

# Troubleshooting dataset lineage

Dataset Lineage lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, dataset lineage is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
