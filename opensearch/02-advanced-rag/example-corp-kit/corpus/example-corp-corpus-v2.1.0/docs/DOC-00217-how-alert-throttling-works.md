---
source_id: "DOC-00217"
title: "How alert throttling works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > How alert throttling works"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2025-05-19"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# How alert throttling works

Alert Throttling is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for alert throttling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: alert throttling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, alert throttling is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
