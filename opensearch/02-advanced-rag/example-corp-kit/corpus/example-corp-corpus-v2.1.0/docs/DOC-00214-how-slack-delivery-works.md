---
source_id: "DOC-00214"
title: "How Slack delivery works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > How Slack delivery works"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2024-08-02"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# How Slack delivery works

Slack Delivery is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When Slack delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for Slack delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, Slack delivery is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
