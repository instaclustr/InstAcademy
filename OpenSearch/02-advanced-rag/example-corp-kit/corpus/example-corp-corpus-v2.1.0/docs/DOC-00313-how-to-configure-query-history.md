---
source_id: "DOC-00313"
title: "How to configure query history"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > How to configure query history"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2024-02-29"
related_error_codes: ["ERR-5501"]
---

# How to configure query history

This page explains how query history works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

By default, query history is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
