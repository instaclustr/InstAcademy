---
source_id: "DOC-00212"
title: "How anomaly alerts works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > How anomaly alerts works"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2024-11-07"
related_error_codes: ["ERR-4415"]
---

# How anomaly alerts works

Anomaly Alerts is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, anomaly alerts inherits group membership from your identity provider on each login.

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for anomaly alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, anomaly alerts is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
