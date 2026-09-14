---
source_id: "DOC-00360"
title: "Query History settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > Query History settings reference"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2025-10-26"
related_error_codes: ["ERR-5501"]
---

# Query History settings reference

Query History is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

By default, query history is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
