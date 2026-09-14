---
source_id: "DOC-00918"
title: "How email delivery works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > How email delivery works"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2024-06-22"
related_error_codes: ["ERR-4415"]
---

# How email delivery works

Email Delivery is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, email delivery is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable email delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, email delivery inherits group membership from your identity provider on each login.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
