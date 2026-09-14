---
source_id: "DOC-00436"
title: "How dataset lineage works"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > How dataset lineage works"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2024-04-20"
related_error_codes: ["ERR-3340"]
---

# How dataset lineage works

Dataset Lineage lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

When dataset lineage is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, dataset lineage is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
