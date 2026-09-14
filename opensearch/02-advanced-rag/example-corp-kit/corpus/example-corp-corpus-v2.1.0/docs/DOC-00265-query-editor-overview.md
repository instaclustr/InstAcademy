---
source_id: "DOC-00265"
title: "Query Editor overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > Query Editor overview"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2026-06-29"
related_error_codes: ["ERR-5501"]
---

# Query Editor overview

Query Editor lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

By default, query editor is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
