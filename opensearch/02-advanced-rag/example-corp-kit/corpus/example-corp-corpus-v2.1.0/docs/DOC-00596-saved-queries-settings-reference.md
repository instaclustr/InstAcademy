---
source_id: "DOC-00596"
title: "Saved Queries settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > Saved Queries settings reference"
product_area: "sql-workbench"
product_version: "4.9"
acl: "standard"
updated_at: "2025-07-29"
related_error_codes: ["ERR-5501"]
---

# Saved Queries settings reference

This page explains how saved queries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
