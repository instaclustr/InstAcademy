---
source_id: "DOC-00316"
title: "How to configure result caching"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > How to configure result caching"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-03-09"
related_error_codes: ["ERR-5501"]
---

# How to configure result caching

Result Caching lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When result caching is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, result caching inherits group membership from your identity provider on each login.

By default, result caching is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: result caching performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
