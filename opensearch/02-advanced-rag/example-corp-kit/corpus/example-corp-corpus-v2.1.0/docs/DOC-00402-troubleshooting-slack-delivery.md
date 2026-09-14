---
source_id: "DOC-00402"
title: "Troubleshooting Slack delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > Troubleshooting Slack delivery"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2025-04-25"
related_error_codes: ["ERR-4415"]
---

# Troubleshooting Slack delivery

Slack Delivery lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

By default, Slack delivery is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, Slack delivery inherits group membership from your identity provider on each login.

Audit events for Slack delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When Slack delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
