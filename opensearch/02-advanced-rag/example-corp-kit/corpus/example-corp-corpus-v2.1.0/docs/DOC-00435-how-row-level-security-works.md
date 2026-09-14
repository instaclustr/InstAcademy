---
source_id: "DOC-00435"
title: "How row-level security works"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > How row-level security works"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2026-04-12"
related_error_codes: ["ERR-3340"]
---

# How row-level security works

Row-Level Security lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

By default, row-level security is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
