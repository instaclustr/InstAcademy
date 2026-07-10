---
source_id: "DOC-00315"
title: "How to configure query timeouts"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > How to configure query timeouts"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2025-06-30"
related_error_codes: ["ERR-5501"]
---

# How to configure query timeouts

Query Timeouts lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When query timeouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: query timeouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, query timeouts inherits group membership from your identity provider on each login.

To enable query timeouts, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

By default, query timeouts is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
