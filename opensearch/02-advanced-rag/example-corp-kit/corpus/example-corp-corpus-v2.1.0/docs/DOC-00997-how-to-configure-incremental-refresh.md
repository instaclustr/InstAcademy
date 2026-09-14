---
source_id: "DOC-00997"
title: "How to configure incremental refresh"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > How to configure incremental refresh"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2026-02-07"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# How to configure incremental refresh

Incremental Refresh lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, incremental refresh inherits group membership from your identity provider on each login.

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: incremental refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for incremental refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable incremental refresh, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
