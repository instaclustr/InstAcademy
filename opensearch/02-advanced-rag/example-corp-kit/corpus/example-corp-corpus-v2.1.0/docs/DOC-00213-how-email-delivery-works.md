---
source_id: "DOC-00213"
title: "How email delivery works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > How email delivery works"
product_area: "alerts"
product_version: "4.9"
acl: "standard"
updated_at: "2025-05-10"
related_error_codes: ["ERR-4415"]
---

# How email delivery works

Email Delivery lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

To enable email delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, email delivery is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, email delivery inherits group membership from your identity provider on each login.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
