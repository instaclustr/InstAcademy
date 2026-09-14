---
source_id: "DOC-00531"
title: "How to configure materialized views"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > How to configure materialized views"
product_area: "datasets"
product_version: "5.0"
acl: "enterprise"
updated_at: "2024-01-23"
related_error_codes: ["ERR-3305"]
---

# How to configure materialized views

Materialized Views lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, materialized views inherits group membership from your identity provider on each login.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, materialized views is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
