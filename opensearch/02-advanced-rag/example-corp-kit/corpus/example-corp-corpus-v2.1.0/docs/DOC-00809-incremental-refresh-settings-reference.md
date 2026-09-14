---
source_id: "DOC-00809"
title: "Incremental Refresh settings reference"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > Incremental Refresh settings reference"
product_area: "datasets"
product_version: "4.9"
acl: "professional"
updated_at: "2025-08-23"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# Incremental Refresh settings reference

Incremental Refresh lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, incremental refresh inherits group membership from your identity provider on each login.

Performance tip: incremental refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable incremental refresh, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for incremental refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
