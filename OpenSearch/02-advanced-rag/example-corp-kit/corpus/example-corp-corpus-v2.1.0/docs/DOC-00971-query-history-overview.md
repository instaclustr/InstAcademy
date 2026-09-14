---
source_id: "DOC-00971"
title: "Query History overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > Query History overview"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2024-10-22"
related_error_codes: ["ERR-5501"]
---

# Query History overview

Query History is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, query history is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
