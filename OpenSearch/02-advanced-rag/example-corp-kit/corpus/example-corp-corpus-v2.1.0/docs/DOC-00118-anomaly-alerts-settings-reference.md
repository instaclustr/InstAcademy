---
source_id: "DOC-00118"
title: "Anomaly Alerts settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > Anomaly Alerts settings reference"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2025-02-21"
related_error_codes: ["ERR-4402"]
---

# Anomaly Alerts settings reference

This page explains how anomaly alerts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, anomaly alerts inherits group membership from your identity provider on each login.

By default, anomaly alerts is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: anomaly alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
