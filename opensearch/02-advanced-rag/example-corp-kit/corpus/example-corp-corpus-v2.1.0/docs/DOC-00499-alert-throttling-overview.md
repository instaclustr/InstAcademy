---
source_id: "DOC-00499"
title: "Alert Throttling overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > Alert Throttling overview"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2024-01-30"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# Alert Throttling overview

Alert Throttling lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, alert throttling is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: alert throttling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
