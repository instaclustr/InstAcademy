---
source_id: "DOC-00813"
title: "Materialized Views settings reference"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > Materialized Views settings reference"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2025-02-24"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# Materialized Views settings reference

This page explains how materialized views works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, materialized views inherits group membership from your identity provider on each login.

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, materialized views is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
