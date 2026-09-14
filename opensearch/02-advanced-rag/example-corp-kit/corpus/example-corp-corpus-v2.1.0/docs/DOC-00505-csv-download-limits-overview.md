---
source_id: "DOC-00505"
title: "Csv Download Limits overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Csv Download Limits > Csv Download Limits overview"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2025-12-19"
related_error_codes: ["ERR-5501"]
---

# Csv Download Limits overview

Csv Download Limits lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

When CSV download limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for CSV download limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: CSV download limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, CSV download limits inherits group membership from your identity provider on each login.

By default, CSV download limits is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
