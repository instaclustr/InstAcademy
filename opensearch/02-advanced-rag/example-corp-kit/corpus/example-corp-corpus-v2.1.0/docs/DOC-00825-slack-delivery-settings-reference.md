---
source_id: "DOC-00825"
title: "Slack Delivery settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > Slack Delivery settings reference"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2026-02-06"
related_error_codes: ["ERR-4402"]
---

# Slack Delivery settings reference

Slack Delivery lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When Slack delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, Slack delivery is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, Slack delivery inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
