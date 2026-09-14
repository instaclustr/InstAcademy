---
source_id: "DOC-00973"
title: "Query Timeouts overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > Query Timeouts overview"
product_area: "sql-workbench"
product_version: "5.0"
acl: "standard"
updated_at: "2026-04-14"
related_error_codes: ["ERR-5501"]
---

# Query Timeouts overview

Query Timeouts lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Audit events for query timeouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When query timeouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable query timeouts, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

By default, query timeouts is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, query timeouts inherits group membership from your identity provider on each login.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
