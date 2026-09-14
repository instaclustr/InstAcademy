---
source_id: "DOC-00598"
title: "Result Caching settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > Result Caching settings reference"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2025-12-16"
related_error_codes: ["ERR-5501"]
---

# Result Caching settings reference

Result Caching lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, result caching is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When result caching is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: result caching performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, result caching inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
