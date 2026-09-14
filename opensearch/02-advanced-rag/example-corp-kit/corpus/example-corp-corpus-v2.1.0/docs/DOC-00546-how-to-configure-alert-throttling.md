---
source_id: "DOC-00546"
title: "How to configure alert throttling"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > How to configure alert throttling"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2025-04-14"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# How to configure alert throttling

This page explains how alert throttling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, alert throttling is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

Performance tip: alert throttling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
