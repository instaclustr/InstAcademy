---
source_id: "DOC-00552"
title: "How to configure CSV download limits"
doc_type: "product-docs"
section_path: "SQL Workbench > Csv Download Limits > How to configure CSV download limits"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-04-01"
related_error_codes: ["ERR-5501"]
---

# How to configure CSV download limits

This page explains how CSV download limits works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: CSV download limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, CSV download limits is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for CSV download limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable CSV download limits, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When CSV download limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
