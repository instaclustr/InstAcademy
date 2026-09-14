---
source_id: "DOC-00594"
title: "Query Editor settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > Query Editor settings reference"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2026-03-29"
related_error_codes: ["ERR-5501"]
---

# Query Editor settings reference

Query Editor is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, query editor is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for query editor are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
