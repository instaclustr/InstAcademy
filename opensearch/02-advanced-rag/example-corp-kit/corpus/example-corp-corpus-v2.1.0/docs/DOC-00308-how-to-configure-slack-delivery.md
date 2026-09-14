---
source_id: "DOC-00308"
title: "How to configure Slack delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > How to configure Slack delivery"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2025-09-08"
related_error_codes: ["ERR-4402"]
---

# How to configure Slack delivery

Slack Delivery lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When Slack delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, Slack delivery is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, Slack delivery inherits group membership from your identity provider on each login.

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
