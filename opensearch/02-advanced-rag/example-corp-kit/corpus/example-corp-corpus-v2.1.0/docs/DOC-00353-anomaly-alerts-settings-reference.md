---
source_id: "DOC-00353"
title: "Anomaly Alerts settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > Anomaly Alerts settings reference"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2025-01-27"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Anomaly Alerts settings reference

Anomaly Alerts is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for anomaly alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: anomaly alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, anomaly alerts is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
