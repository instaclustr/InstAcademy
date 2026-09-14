---
source_id: "DOC-00591"
title: "Webhook Delivery settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > Webhook Delivery settings reference"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2026-06-02"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Webhook Delivery settings reference

Webhook Delivery is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, webhook delivery is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for webhook delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable webhook delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, webhook delivery inherits group membership from your identity provider on each login.

When webhook delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
