---
source_id: "DOC-00917"
title: "How anomaly alerts works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > How anomaly alerts works"
product_area: "alerts"
product_version: "5.1"
acl: "professional"
updated_at: "2026-06-03"
related_error_codes: ["ERR-4415"]
---

# How anomaly alerts works

This page explains how anomaly alerts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for anomaly alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, anomaly alerts is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: anomaly alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, anomaly alerts inherits group membership from your identity provider on each login.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
