---
source_id: "DOC-00787"
title: "How to configure CSV download limits"
doc_type: "product-docs"
section_path: "SQL Workbench > Csv Download Limits > How to configure CSV download limits"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-03-05"
related_error_codes: ["ERR-5501"]
---

# How to configure CSV download limits

This page explains how CSV download limits works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, CSV download limits inherits group membership from your identity provider on each login.

To enable CSV download limits, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

By default, CSV download limits is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When CSV download limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: CSV download limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
