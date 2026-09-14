---
source_id: "DOC-00684"
title: "How Slack delivery works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > How Slack delivery works"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2024-10-04"
related_error_codes: ["ERR-4415"]
---

# How Slack delivery works

Slack Delivery lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When Slack delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, Slack delivery is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, Slack delivery inherits group membership from your identity provider on each login.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
