---
source_id: "DOC-00829"
title: "Query Editor settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > Query Editor settings reference"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2025-03-13"
related_error_codes: ["ERR-5501"]
---

# Query Editor settings reference

Query Editor lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for query editor are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
