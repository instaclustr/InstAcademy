---
source_id: "DOC-00729"
title: "Anomaly Alerts overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > Anomaly Alerts overview"
product_area: "alerts"
product_version: "4.9"
acl: "enterprise"
updated_at: "2024-08-16"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# Anomaly Alerts overview

Anomaly Alerts is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for anomaly alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, anomaly alerts is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, anomaly alerts inherits group membership from your identity provider on each login.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
