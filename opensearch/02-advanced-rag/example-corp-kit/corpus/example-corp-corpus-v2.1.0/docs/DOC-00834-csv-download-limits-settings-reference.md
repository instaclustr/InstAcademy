---
source_id: "DOC-00834"
title: "Csv Download Limits settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Csv Download Limits > Csv Download Limits settings reference"
product_area: "sql-workbench"
product_version: "5.1"
acl: "public"
updated_at: "2026-03-21"
related_error_codes: ["ERR-5501"]
---

# Csv Download Limits settings reference

Csv Download Limits lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

When CSV download limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable CSV download limits, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: CSV download limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, CSV download limits is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, CSV download limits inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
