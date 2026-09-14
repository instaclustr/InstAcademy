---
source_id: "DOC-00786"
title: "How to configure result caching"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > How to configure result caching"
product_area: "sql-workbench"
product_version: "5.1"
acl: "professional"
updated_at: "2025-05-13"
related_error_codes: ["ERR-5501"]
---

# How to configure result caching

Result Caching is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: result caching performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable result caching, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When result caching is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, result caching is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
