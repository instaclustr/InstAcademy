---
source_id: "DOC-00635"
title: "Troubleshooting anomaly alerts"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > Troubleshooting anomaly alerts"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2025-05-15"
related_error_codes: ["ERR-4402"]
---

# Troubleshooting anomaly alerts

Anomaly Alerts lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, anomaly alerts inherits group membership from your identity provider on each login.

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, anomaly alerts is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for anomaly alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
