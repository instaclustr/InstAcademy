---
source_id: "DOC-00828"
title: "Alert Throttling settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > Alert Throttling settings reference"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2024-12-10"
related_error_codes: ["ERR-4415"]
---

# Alert Throttling settings reference

Alert Throttling lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

Performance tip: alert throttling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, alert throttling is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
