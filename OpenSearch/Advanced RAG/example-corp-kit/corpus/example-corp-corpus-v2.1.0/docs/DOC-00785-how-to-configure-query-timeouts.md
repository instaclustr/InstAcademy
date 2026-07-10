---
source_id: "DOC-00785"
title: "How to configure query timeouts"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > How to configure query timeouts"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2024-12-29"
related_error_codes: ["ERR-5501"]
---

# How to configure query timeouts

Query Timeouts is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, query timeouts inherits group membership from your identity provider on each login.

Audit events for query timeouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, query timeouts is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable query timeouts, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: query timeouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
