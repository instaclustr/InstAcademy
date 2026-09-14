---
source_id: "DOC-00075"
title: "How to configure report bursting"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > How to configure report bursting"
product_area: "alerts"
product_version: "4.9"
acl: "enterprise"
updated_at: "2024-08-19"
related_error_codes: ["ERR-4415"]
---

# How to configure report bursting

Report Bursting lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for report bursting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, report bursting is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
