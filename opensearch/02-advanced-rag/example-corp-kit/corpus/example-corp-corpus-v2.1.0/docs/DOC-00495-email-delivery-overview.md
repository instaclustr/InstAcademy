---
source_id: "DOC-00495"
title: "Email Delivery overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > Email Delivery overview"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2026-02-25"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Email Delivery overview

This page explains how email delivery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable email delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, email delivery is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
