---
source_id: "DOC-00126"
title: "Saved Queries settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > Saved Queries settings reference"
product_area: "sql-workbench"
product_version: "5.1"
acl: "professional"
updated_at: "2025-07-30"
related_error_codes: ["ERR-5501"]
---

# Saved Queries settings reference

Saved Queries lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

By default, saved queries is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
