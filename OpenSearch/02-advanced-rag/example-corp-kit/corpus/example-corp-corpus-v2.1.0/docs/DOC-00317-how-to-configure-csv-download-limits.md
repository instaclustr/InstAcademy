---
source_id: "DOC-00317"
title: "How to configure CSV download limits"
doc_type: "product-docs"
section_path: "SQL Workbench > Csv Download Limits > How to configure CSV download limits"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2025-02-24"
related_error_codes: ["ERR-5501"]
---

# How to configure CSV download limits

This page explains how CSV download limits works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When CSV download limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, CSV download limits is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: CSV download limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, CSV download limits inherits group membership from your identity provider on each login.

Audit events for CSV download limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
