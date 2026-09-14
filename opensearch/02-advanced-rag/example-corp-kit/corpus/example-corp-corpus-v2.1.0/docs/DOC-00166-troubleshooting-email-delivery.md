---
source_id: "DOC-00166"
title: "Troubleshooting email delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > Troubleshooting email delivery"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2024-04-14"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# Troubleshooting email delivery

This page explains how email delivery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable email delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, email delivery is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
