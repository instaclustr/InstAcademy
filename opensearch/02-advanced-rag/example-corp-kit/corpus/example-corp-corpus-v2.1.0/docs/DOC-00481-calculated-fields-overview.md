---
source_id: "DOC-00481"
title: "Calculated Fields overview"
doc_type: "product-docs"
section_path: "Datasets > Calculated Fields > Calculated Fields overview"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2024-02-29"
related_error_codes: ["ERR-3340"]
---

# Calculated Fields overview

Calculated Fields is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, calculated fields inherits group membership from your identity provider on each login.

Audit events for calculated fields are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable calculated fields, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: calculated fields performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When calculated fields is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
