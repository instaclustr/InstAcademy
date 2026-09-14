---
source_id: "DOC-00595"
title: "Query History settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > Query History settings reference"
product_area: "sql-workbench"
product_version: "4.9"
acl: "standard"
updated_at: "2026-03-20"
related_error_codes: ["ERR-5501"]
---

# Query History settings reference

Query History is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
