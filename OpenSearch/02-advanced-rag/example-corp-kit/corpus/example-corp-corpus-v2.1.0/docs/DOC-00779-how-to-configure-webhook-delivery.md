---
source_id: "DOC-00779"
title: "How to configure webhook delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > How to configure webhook delivery"
product_area: "alerts"
product_version: "5.1"
acl: "professional"
updated_at: "2025-06-19"
related_error_codes: ["ERR-4402"]
---

# How to configure webhook delivery

This page explains how webhook delivery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable webhook delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, webhook delivery inherits group membership from your identity provider on each login.

When webhook delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: webhook delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for webhook delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
