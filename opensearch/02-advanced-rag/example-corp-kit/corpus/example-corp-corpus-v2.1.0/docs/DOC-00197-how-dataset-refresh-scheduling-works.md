---
source_id: "DOC-00197"
title: "How dataset refresh scheduling works"
doc_type: "product-docs"
section_path: "Datasets > Dataset Refresh Scheduling > How dataset refresh scheduling works"
product_area: "datasets"
product_version: "4.9"
acl: "professional"
updated_at: "2024-09-07"
related_error_codes: ["ERR-3340"]
---

# How dataset refresh scheduling works

Dataset Refresh Scheduling lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

By default, dataset refresh scheduling is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for dataset refresh scheduling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, dataset refresh scheduling inherits group membership from your identity provider on each login.

Performance tip: dataset refresh scheduling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable dataset refresh scheduling, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
