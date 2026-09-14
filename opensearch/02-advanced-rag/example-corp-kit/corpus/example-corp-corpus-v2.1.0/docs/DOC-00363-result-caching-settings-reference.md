---
source_id: "DOC-00363"
title: "Result Caching settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > Result Caching settings reference"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2024-10-22"
related_error_codes: ["ERR-5501"]
---

# Result Caching settings reference

Result Caching lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

When result caching is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, result caching inherits group membership from your identity provider on each login.

To enable result caching, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: result caching performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
