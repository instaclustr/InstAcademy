---
source_id: "DOC-00782"
title: "How to configure query editor"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > How to configure query editor"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2026-03-20"
related_error_codes: ["ERR-5501"]
---

# How to configure query editor

Query Editor lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

By default, query editor is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
