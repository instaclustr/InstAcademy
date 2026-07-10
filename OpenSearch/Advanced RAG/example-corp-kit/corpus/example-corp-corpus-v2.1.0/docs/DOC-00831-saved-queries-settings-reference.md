---
source_id: "DOC-00831"
title: "Saved Queries settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > Saved Queries settings reference"
product_area: "sql-workbench"
product_version: "5.1"
acl: "public"
updated_at: "2025-05-23"
related_error_codes: ["ERR-5501"]
---

# Saved Queries settings reference

Saved Queries lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
