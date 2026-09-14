---
source_id: "DOC-00824"
title: "Email Delivery settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > Email Delivery settings reference"
product_area: "alerts"
product_version: "5.0"
acl: "professional"
updated_at: "2026-02-19"
related_error_codes: ["ERR-4402"]
---

# Email Delivery settings reference

This page explains how email delivery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable email delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, email delivery is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, email delivery inherits group membership from your identity provider on each login.

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
