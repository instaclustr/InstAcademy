---
source_id: "DOC-00832"
title: "Query Timeouts settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > Query Timeouts settings reference"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2026-05-10"
related_error_codes: ["ERR-5501"]
---

# Query Timeouts settings reference

Query Timeouts is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, query timeouts inherits group membership from your identity provider on each login.

Performance tip: query timeouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable query timeouts, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

By default, query timeouts is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for query timeouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
