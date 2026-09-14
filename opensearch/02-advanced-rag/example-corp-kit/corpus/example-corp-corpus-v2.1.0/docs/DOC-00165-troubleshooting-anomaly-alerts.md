---
source_id: "DOC-00165"
title: "Troubleshooting anomaly alerts"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > Troubleshooting anomaly alerts"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2025-01-27"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Troubleshooting anomaly alerts

Anomaly Alerts lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Audit events for anomaly alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, anomaly alerts is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, anomaly alerts inherits group membership from your identity provider on each login.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
