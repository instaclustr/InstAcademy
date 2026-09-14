---
source_id: "DOC-00076"
title: "How to configure alert throttling"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > How to configure alert throttling"
product_area: "alerts"
product_version: "5.0"
acl: "enterprise"
updated_at: "2024-03-19"
related_error_codes: ["ERR-4415"]
---

# How to configure alert throttling

Alert Throttling lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Performance tip: alert throttling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

By default, alert throttling is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
