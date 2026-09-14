---
source_id: "DOC-00268"
title: "Query Timeouts overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > Query Timeouts overview"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2026-01-29"
related_error_codes: ["ERR-5501"]
---

# Query Timeouts overview

Query Timeouts lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

Performance tip: query timeouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for query timeouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, query timeouts is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When query timeouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, query timeouts inherits group membership from your identity provider on each login.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
