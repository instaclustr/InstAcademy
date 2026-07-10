---
source_id: "DOC-00081"
title: "How to configure result caching"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > How to configure result caching"
product_area: "sql-workbench"
product_version: "4.8"
acl: "enterprise"
updated_at: "2024-03-23"
related_error_codes: ["ERR-5501"]
---

# How to configure result caching

This page explains how result caching works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When result caching is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable result caching, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, result caching inherits group membership from your identity provider on each login.

By default, result caching is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
