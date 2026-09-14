---
source_id: "DOC-00015"
title: "Refresh Failure Retries overview"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > Refresh Failure Retries overview"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2025-10-29"
related_error_codes: ["ERR-3340"]
---

# Refresh Failure Retries overview

This page explains how refresh failure retries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

When refresh failure retries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, refresh failure retries is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
