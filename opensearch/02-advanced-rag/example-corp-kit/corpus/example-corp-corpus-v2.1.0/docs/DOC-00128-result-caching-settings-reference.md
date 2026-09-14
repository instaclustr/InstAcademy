---
source_id: "DOC-00128"
title: "Result Caching settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > Result Caching settings reference"
product_area: "sql-workbench"
product_version: "4.9"
acl: "enterprise"
updated_at: "2025-04-17"
related_error_codes: ["ERR-5501"]
---

# Result Caching settings reference

Result Caching lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

To enable result caching, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, result caching inherits group membership from your identity provider on each login.

By default, result caching is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: result caching performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
