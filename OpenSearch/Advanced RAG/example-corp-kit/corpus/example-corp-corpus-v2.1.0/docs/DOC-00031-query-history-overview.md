---
source_id: "DOC-00031"
title: "Query History overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > Query History overview"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-05-06"
related_error_codes: ["ERR-5501"]
---

# Query History overview

Query History lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

By default, query history is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
