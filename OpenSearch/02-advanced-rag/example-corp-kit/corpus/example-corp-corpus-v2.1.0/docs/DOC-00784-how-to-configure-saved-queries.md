---
source_id: "DOC-00784"
title: "How to configure saved queries"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > How to configure saved queries"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2025-01-27"
related_error_codes: ["ERR-5501"]
---

# How to configure saved queries

Saved Queries is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, saved queries is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
