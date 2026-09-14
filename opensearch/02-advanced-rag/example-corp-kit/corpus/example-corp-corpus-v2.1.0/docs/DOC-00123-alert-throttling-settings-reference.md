---
source_id: "DOC-00123"
title: "Alert Throttling settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > Alert Throttling settings reference"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2024-12-27"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# Alert Throttling settings reference

Alert Throttling lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

Audit events for alert throttling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: alert throttling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
