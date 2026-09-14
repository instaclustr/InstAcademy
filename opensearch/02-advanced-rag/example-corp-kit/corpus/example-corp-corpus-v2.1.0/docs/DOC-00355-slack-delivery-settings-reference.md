---
source_id: "DOC-00355"
title: "Slack Delivery settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > Slack Delivery settings reference"
product_area: "alerts"
product_version: "4.8"
acl: "standard"
updated_at: "2024-05-03"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Slack Delivery settings reference

This page explains how Slack delivery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, Slack delivery inherits group membership from your identity provider on each login.

Audit events for Slack delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When Slack delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
