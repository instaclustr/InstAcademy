---
source_id: "DOC-00155"
title: "Troubleshooting materialized views"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > Troubleshooting materialized views"
product_area: "datasets"
product_version: "4.8"
acl: "professional"
updated_at: "2025-02-01"
related_error_codes: ["ERR-3340"]
---

# Troubleshooting materialized views

Materialized Views is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, materialized views inherits group membership from your identity provider on each login.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, materialized views is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
