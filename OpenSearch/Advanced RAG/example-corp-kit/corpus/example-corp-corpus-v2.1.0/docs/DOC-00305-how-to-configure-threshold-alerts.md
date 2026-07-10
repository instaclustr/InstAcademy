---
source_id: "DOC-00305"
title: "How to configure threshold alerts"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > How to configure threshold alerts"
product_area: "alerts"
product_version: "5.0"
acl: "standard"
updated_at: "2025-10-29"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# How to configure threshold alerts

Threshold Alerts lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Performance tip: threshold alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for threshold alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, threshold alerts is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable threshold alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
