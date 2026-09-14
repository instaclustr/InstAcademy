---
source_id: "DOC-00403"
title: "Troubleshooting webhook delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > Troubleshooting webhook delivery"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2026-02-27"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Troubleshooting webhook delivery

Webhook Delivery lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

When webhook delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, webhook delivery inherits group membership from your identity provider on each login.

By default, webhook delivery is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable webhook delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: webhook delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
