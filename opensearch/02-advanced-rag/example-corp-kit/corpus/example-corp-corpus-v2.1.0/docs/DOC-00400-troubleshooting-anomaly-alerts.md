---
source_id: "DOC-00400"
title: "Troubleshooting anomaly alerts"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > Troubleshooting anomaly alerts"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2024-10-17"
related_error_codes: ["ERR-4415"]
---

# Troubleshooting anomaly alerts

Anomaly Alerts lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for anomaly alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: anomaly alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, anomaly alerts inherits group membership from your identity provider on each login.

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
