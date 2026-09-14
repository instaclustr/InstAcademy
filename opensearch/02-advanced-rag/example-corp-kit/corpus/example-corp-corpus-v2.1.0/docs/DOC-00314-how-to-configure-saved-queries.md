---
source_id: "DOC-00314"
title: "How to configure saved queries"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > How to configure saved queries"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2026-06-01"
related_error_codes: ["ERR-5501"]
---

# How to configure saved queries

This page explains how saved queries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, saved queries is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
