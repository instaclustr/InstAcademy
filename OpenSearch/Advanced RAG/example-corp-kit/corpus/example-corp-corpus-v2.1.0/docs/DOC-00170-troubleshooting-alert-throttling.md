---
source_id: "DOC-00170"
title: "Troubleshooting alert throttling"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > Troubleshooting alert throttling"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2025-02-14"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Troubleshooting alert throttling

Alert Throttling lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

Performance tip: alert throttling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, alert throttling is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for alert throttling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
