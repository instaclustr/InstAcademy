---
source_id: "DOC-00527"
title: "How to configure incremental refresh"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > How to configure incremental refresh"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2024-11-11"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# How to configure incremental refresh

This page explains how incremental refresh works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable incremental refresh, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, incremental refresh inherits group membership from your identity provider on each login.

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, incremental refresh is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: incremental refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
