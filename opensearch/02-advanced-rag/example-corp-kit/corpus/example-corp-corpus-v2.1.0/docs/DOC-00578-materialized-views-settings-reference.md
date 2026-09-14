---
source_id: "DOC-00578"
title: "Materialized Views settings reference"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > Materialized Views settings reference"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2025-09-03"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# Materialized Views settings reference

This page explains how materialized views works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, materialized views inherits group membership from your identity provider on each login.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
