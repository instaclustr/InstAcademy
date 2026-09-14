---
source_id: "DOC-00766"
title: "How to configure materialized views"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > How to configure materialized views"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2025-09-01"
related_error_codes: ["ERR-3305"]
---

# How to configure materialized views

Materialized Views is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, materialized views inherits group membership from your identity provider on each login.

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
