---
source_id: "DOC-00312"
title: "How to configure query editor"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > How to configure query editor"
product_area: "sql-workbench"
product_version: "5.1"
acl: "public"
updated_at: "2024-06-14"
related_error_codes: ["ERR-5501"]
---

# How to configure query editor

Query Editor lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Audit events for query editor are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

By default, query editor is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
