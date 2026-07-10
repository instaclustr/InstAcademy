---
source_id: "DOC-00388"
title: "Troubleshooting row-level security"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > Troubleshooting row-level security"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2025-06-19"
related_error_codes: ["ERR-3340"]
---

# Troubleshooting row-level security

This page explains how row-level security works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, row-level security is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
