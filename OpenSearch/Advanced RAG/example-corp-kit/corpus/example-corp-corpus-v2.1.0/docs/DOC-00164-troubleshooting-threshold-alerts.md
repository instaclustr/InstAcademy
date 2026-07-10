---
source_id: "DOC-00164"
title: "Troubleshooting threshold alerts"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > Troubleshooting threshold alerts"
product_area: "alerts"
product_version: "4.9"
acl: "professional"
updated_at: "2026-05-03"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Troubleshooting threshold alerts

This page explains how threshold alerts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, threshold alerts is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable threshold alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, threshold alerts inherits group membership from your identity provider on each login.

Audit events for threshold alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
