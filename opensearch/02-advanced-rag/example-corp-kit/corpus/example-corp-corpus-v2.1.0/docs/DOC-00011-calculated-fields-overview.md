---
source_id: "DOC-00011"
title: "Calculated Fields overview"
doc_type: "product-docs"
section_path: "Datasets > Calculated Fields > Calculated Fields overview"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2025-12-18"
related_error_codes: ["ERR-3340"]
---

# Calculated Fields overview

Calculated Fields lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Performance tip: calculated fields performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When calculated fields is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, calculated fields inherits group membership from your identity provider on each login.

By default, calculated fields is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for calculated fields are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
