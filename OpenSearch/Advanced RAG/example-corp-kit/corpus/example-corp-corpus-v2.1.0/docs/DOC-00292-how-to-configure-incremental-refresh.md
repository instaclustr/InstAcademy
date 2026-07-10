---
source_id: "DOC-00292"
title: "How to configure incremental refresh"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > How to configure incremental refresh"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2024-12-30"
related_error_codes: ["ERR-3305"]
---

# How to configure incremental refresh

Incremental Refresh lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, incremental refresh is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for incremental refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, incremental refresh inherits group membership from your identity provider on each login.

To enable incremental refresh, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
