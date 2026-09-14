---
source_id: "DOC-00359"
title: "Query Editor settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > Query Editor settings reference"
product_area: "sql-workbench"
product_version: "5.0"
acl: "enterprise"
updated_at: "2024-03-21"
related_error_codes: ["ERR-5501"]
---

# Query Editor settings reference

This page explains how query editor works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for query editor are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

By default, query editor is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
