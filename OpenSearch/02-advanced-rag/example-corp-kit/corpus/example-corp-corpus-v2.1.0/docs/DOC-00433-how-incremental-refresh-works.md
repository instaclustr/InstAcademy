---
source_id: "DOC-00433"
title: "How incremental refresh works"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > How incremental refresh works"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2025-12-20"
related_error_codes: ["ERR-3340"]
---

# How incremental refresh works

This page explains how incremental refresh works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, incremental refresh is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for incremental refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, incremental refresh inherits group membership from your identity provider on each login.

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: incremental refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
