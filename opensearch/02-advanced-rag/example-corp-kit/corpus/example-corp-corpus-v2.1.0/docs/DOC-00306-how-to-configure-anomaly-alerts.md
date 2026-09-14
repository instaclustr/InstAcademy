---
source_id: "DOC-00306"
title: "How to configure anomaly alerts"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > How to configure anomaly alerts"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2025-03-19"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# How to configure anomaly alerts

Anomaly Alerts lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

By default, anomaly alerts is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: anomaly alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for anomaly alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
