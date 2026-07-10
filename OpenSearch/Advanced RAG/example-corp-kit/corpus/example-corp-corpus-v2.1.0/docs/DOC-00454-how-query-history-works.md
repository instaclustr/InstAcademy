---
source_id: "DOC-00454"
title: "How query history works"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > How query history works"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2025-08-31"
related_error_codes: ["ERR-5501"]
---

# How query history works

Query History is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, query history is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
