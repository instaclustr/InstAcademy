---
source_id: "DOC-00830"
title: "Query History settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > Query History settings reference"
product_area: "sql-workbench"
product_version: "4.8"
acl: "professional"
updated_at: "2026-06-13"
related_error_codes: ["ERR-5501"]
---

# Query History settings reference

This page explains how query history works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

By default, query history is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
