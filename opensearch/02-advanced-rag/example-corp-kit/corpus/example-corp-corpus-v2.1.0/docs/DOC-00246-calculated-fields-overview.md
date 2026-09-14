---
source_id: "DOC-00246"
title: "Calculated Fields overview"
doc_type: "product-docs"
section_path: "Datasets > Calculated Fields > Calculated Fields overview"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2026-04-18"
related_error_codes: ["ERR-3340"]
---

# Calculated Fields overview

This page explains how calculated fields works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, calculated fields inherits group membership from your identity provider on each login.

Audit events for calculated fields are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable calculated fields, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: calculated fields performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, calculated fields is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
