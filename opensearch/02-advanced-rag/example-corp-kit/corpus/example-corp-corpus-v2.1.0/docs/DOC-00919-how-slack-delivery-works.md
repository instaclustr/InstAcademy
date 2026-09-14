---
source_id: "DOC-00919"
title: "How Slack delivery works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > How Slack delivery works"
product_area: "alerts"
product_version: "4.9"
acl: "professional"
updated_at: "2024-07-14"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# How Slack delivery works

Slack Delivery lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Audit events for Slack delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, Slack delivery inherits group membership from your identity provider on each login.

By default, Slack delivery is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
