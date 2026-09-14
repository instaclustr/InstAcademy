---
source_id: "DOC-00682"
title: "How anomaly alerts works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > How anomaly alerts works"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2026-05-19"
related_error_codes: ["ERR-4415"]
---

# How anomaly alerts works

Anomaly Alerts lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

By default, anomaly alerts is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, anomaly alerts inherits group membership from your identity provider on each login.

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: anomaly alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
