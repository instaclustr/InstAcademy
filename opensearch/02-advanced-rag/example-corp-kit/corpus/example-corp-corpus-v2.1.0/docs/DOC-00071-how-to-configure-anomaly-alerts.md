---
source_id: "DOC-00071"
title: "How to configure anomaly alerts"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > How to configure anomaly alerts"
product_area: "alerts"
product_version: "4.9"
acl: "professional"
updated_at: "2024-03-01"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# How to configure anomaly alerts

Anomaly Alerts lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Performance tip: anomaly alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, anomaly alerts inherits group membership from your identity provider on each login.

By default, anomaly alerts is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for anomaly alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
