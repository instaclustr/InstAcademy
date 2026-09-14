---
source_id: "DOC-00391"
title: "Troubleshooting refresh failure retries"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > Troubleshooting refresh failure retries"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2025-08-14"
related_error_codes: ["ERR-3340"]
---

# Troubleshooting refresh failure retries

This page explains how refresh failure retries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, refresh failure retries is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
