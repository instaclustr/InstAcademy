---
source_id: "DOC-00544"
title: "How to configure webhook delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > How to configure webhook delivery"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2024-05-16"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# How to configure webhook delivery

Webhook Delivery lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, webhook delivery inherits group membership from your identity provider on each login.

By default, webhook delivery is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: webhook delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When webhook delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for webhook delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
