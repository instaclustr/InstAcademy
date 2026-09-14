---
source_id: "DOC-00294"
title: "How to configure row-level security"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > How to configure row-level security"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2024-08-30"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# How to configure row-level security

This page explains how row-level security works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, row-level security is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
