---
source_id: "DOC-00783"
title: "How to configure query history"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > How to configure query history"
product_area: "sql-workbench"
product_version: "4.9"
acl: "standard"
updated_at: "2025-08-23"
related_error_codes: ["ERR-5501"]
---

# How to configure query history

Query History lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, query history is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
