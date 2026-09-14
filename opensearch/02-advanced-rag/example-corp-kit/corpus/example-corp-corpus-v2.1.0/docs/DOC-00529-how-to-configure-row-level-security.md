---
source_id: "DOC-00529"
title: "How to configure row-level security"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > How to configure row-level security"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2024-12-15"
related_error_codes: ["ERR-3305"]
---

# How to configure row-level security

Row-Level Security lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, row-level security is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
