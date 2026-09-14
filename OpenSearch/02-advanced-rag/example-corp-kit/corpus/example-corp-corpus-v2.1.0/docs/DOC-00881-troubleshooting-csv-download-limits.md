---
source_id: "DOC-00881"
title: "Troubleshooting CSV download limits"
doc_type: "product-docs"
section_path: "SQL Workbench > Csv Download Limits > Troubleshooting CSV download limits"
product_area: "sql-workbench"
product_version: "5.1"
acl: "standard"
updated_at: "2026-02-09"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting CSV download limits

Csv Download Limits lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When CSV download limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable CSV download limits, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: CSV download limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, CSV download limits is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, CSV download limits inherits group membership from your identity provider on each login.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
