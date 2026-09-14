---
source_id: "DOC-00668"
title: "How incremental refresh works"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > How incremental refresh works"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2026-06-16"
related_error_codes: ["ERR-3340"]
---

# How incremental refresh works

Incremental Refresh is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, incremental refresh is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for incremental refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, incremental refresh inherits group membership from your identity provider on each login.

To enable incremental refresh, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
