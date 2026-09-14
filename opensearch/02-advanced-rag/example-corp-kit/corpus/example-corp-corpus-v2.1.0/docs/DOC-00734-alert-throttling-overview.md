---
source_id: "DOC-00734"
title: "Alert Throttling overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > Alert Throttling overview"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2026-03-12"
related_error_codes: ["ERR-4415"]
---

# Alert Throttling overview

Alert Throttling is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for alert throttling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, alert throttling is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
