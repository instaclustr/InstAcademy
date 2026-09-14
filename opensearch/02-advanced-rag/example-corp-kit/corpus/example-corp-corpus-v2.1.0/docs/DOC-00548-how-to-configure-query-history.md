---
source_id: "DOC-00548"
title: "How to configure query history"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > How to configure query history"
product_area: "sql-workbench"
product_version: "5.1"
acl: "public"
updated_at: "2026-04-23"
related_error_codes: ["ERR-5501"]
---

# How to configure query history

Query History is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, query history is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
