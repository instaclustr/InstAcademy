---
source_id: "DOC-00693"
title: "How CSV download limits works"
doc_type: "product-docs"
section_path: "SQL Workbench > Csv Download Limits > How CSV download limits works"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-08-22"
related_error_codes: ["ERR-5501"]
---

# How CSV download limits works

Csv Download Limits lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Audit events for CSV download limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When CSV download limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, CSV download limits inherits group membership from your identity provider on each login.

By default, CSV download limits is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: CSV download limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
