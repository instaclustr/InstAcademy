---
source_id: "DOC-00690"
title: "How saved queries works"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > How saved queries works"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2024-03-08"
related_error_codes: ["ERR-5501"]
---

# How saved queries works

Saved Queries lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
