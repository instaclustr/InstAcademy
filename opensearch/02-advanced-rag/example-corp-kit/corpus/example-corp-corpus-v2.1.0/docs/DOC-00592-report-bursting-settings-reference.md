---
source_id: "DOC-00592"
title: "Report Bursting settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > Report Bursting settings reference"
product_area: "alerts"
product_version: "5.1"
acl: "enterprise"
updated_at: "2026-06-16"
related_error_codes: ["ERR-4415"]
---

# Report Bursting settings reference

Report Bursting lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

By default, report bursting is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for report bursting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
