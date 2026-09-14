---
source_id: "DOC-00543"
title: "How to configure Slack delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > How to configure Slack delivery"
product_area: "alerts"
product_version: "4.9"
acl: "professional"
updated_at: "2024-06-19"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# How to configure Slack delivery

Slack Delivery is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, Slack delivery is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When Slack delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, Slack delivery inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
