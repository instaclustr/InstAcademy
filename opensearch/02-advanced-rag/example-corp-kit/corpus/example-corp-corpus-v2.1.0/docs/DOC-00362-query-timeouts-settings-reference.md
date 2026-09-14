---
source_id: "DOC-00362"
title: "Query Timeouts settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > Query Timeouts settings reference"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-11-09"
related_error_codes: ["ERR-5501"]
---

# Query Timeouts settings reference

Query Timeouts is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: query timeouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, query timeouts inherits group membership from your identity provider on each login.

Audit events for query timeouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable query timeouts, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When query timeouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
