---
source_id: "DOC-00025"
title: "Email Delivery overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > Email Delivery overview"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2025-11-18"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Email Delivery overview

Email Delivery is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable email delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, email delivery is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, email delivery inherits group membership from your identity provider on each login.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
