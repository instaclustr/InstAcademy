---
source_id: "DOC-00108"
title: "Materialized Views settings reference"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > Materialized Views settings reference"
product_area: "datasets"
product_version: "5.0"
acl: "standard"
updated_at: "2026-06-13"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# Materialized Views settings reference

Materialized Views is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, materialized views is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, materialized views inherits group membership from your identity provider on each login.

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
