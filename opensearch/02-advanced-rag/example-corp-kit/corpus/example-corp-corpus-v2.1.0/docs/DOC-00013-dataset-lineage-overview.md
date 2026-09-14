---
source_id: "DOC-00013"
title: "Dataset Lineage overview"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > Dataset Lineage overview"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2026-01-13"
related_error_codes: ["ERR-3340"]
---

# Dataset Lineage overview

Dataset Lineage lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

When dataset lineage is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

By default, dataset lineage is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
