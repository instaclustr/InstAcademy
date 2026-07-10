---
source_id: "DOC-00356"
title: "Webhook Delivery settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > Webhook Delivery settings reference"
product_area: "alerts"
product_version: "5.1"
acl: "standard"
updated_at: "2024-05-11"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# Webhook Delivery settings reference

This page explains how webhook delivery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable webhook delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, webhook delivery is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When webhook delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for webhook delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, webhook delivery inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
