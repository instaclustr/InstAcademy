---
source_id: "DOC-00117"
title: "Threshold Alerts settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > Threshold Alerts settings reference"
product_area: "alerts"
product_version: "4.9"
acl: "enterprise"
updated_at: "2024-08-26"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Threshold Alerts settings reference

This page explains how threshold alerts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, threshold alerts inherits group membership from your identity provider on each login.

Audit events for threshold alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable threshold alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, threshold alerts is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
