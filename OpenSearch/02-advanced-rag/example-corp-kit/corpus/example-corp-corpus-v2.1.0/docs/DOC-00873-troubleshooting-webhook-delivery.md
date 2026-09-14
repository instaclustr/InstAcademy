---
source_id: "DOC-00873"
title: "Troubleshooting webhook delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > Troubleshooting webhook delivery"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2025-02-07"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# Troubleshooting webhook delivery

Webhook Delivery is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable webhook delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, webhook delivery inherits group membership from your identity provider on each login.

Audit events for webhook delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When webhook delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, webhook delivery is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
