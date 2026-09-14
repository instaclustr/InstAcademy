---
source_id: "DOC-00952"
title: "Row-Level Security overview"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > Row-Level Security overview"
product_area: "datasets"
product_version: "4.8"
acl: "professional"
updated_at: "2024-11-06"
related_error_codes: ["ERR-3340"]
---

# Row-Level Security overview

Row-Level Security is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, row-level security is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
