---
source_id: "DOC-00626"
title: "Troubleshooting refresh failure retries"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > Troubleshooting refresh failure retries"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2025-10-02"
related_error_codes: ["ERR-3340"]
---

# Troubleshooting refresh failure retries

This page explains how refresh failure retries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When refresh failure retries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, refresh failure retries is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
