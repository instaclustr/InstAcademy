---
source_id: "DOC-00907"
title: "How materialized views works"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > How materialized views works"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2024-09-14"
related_error_codes: ["ERR-3340"]
---

# How materialized views works

Materialized Views is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, materialized views inherits group membership from your identity provider on each login.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, materialized views is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
