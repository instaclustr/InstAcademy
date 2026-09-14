---
source_id: "DOC-00550"
title: "How to configure query timeouts"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > How to configure query timeouts"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2025-09-06"
related_error_codes: ["ERR-5501"]
---

# How to configure query timeouts

Query Timeouts is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: query timeouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable query timeouts, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When query timeouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, query timeouts is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, query timeouts inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
