---
source_id: "DOC-00358"
title: "Alert Throttling settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > Alert Throttling settings reference"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2025-05-24"
related_error_codes: ["ERR-4415"]
---

# Alert Throttling settings reference

Alert Throttling is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, alert throttling is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for alert throttling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
