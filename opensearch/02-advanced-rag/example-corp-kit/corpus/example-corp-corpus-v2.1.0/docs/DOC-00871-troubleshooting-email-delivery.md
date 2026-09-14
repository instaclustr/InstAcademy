---
source_id: "DOC-00871"
title: "Troubleshooting email delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > Troubleshooting email delivery"
product_area: "alerts"
product_version: "4.8"
acl: "enterprise"
updated_at: "2024-12-23"
related_error_codes: ["ERR-4415"]
---

# Troubleshooting email delivery

Email Delivery is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, email delivery is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable email delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, email delivery inherits group membership from your identity provider on each login.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
