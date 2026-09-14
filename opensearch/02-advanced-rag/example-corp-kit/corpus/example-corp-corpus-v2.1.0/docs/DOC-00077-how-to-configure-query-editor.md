---
source_id: "DOC-00077"
title: "How to configure query editor"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > How to configure query editor"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-01-30"
related_error_codes: ["ERR-5501"]
---

# How to configure query editor

Query Editor is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

By default, query editor is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
