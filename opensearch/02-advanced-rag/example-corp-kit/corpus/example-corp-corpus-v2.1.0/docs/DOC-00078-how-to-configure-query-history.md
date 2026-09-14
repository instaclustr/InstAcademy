---
source_id: "DOC-00078"
title: "How to configure query history"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > How to configure query history"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2026-03-17"
related_error_codes: ["ERR-5501"]
---

# How to configure query history

This page explains how query history works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, query history is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
