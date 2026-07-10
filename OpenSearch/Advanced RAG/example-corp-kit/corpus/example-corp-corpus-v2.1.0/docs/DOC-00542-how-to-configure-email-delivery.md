---
source_id: "DOC-00542"
title: "How to configure email delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > How to configure email delivery"
product_area: "alerts"
product_version: "4.8"
acl: "standard"
updated_at: "2026-02-15"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# How to configure email delivery

Email Delivery is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, email delivery is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, email delivery inherits group membership from your identity provider on each login.

To enable email delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
