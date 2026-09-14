---
source_id: "DOC-00924"
title: "How query history works"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > How query history works"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2026-03-15"
related_error_codes: ["ERR-5501"]
---

# How query history works

Query History lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, query history is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
