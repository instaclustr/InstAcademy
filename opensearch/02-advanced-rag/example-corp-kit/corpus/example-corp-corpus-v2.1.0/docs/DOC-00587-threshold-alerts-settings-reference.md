---
source_id: "DOC-00587"
title: "Threshold Alerts settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > Threshold Alerts settings reference"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2024-07-01"
related_error_codes: ["ERR-4402"]
---

# Threshold Alerts settings reference

This page explains how threshold alerts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable threshold alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for threshold alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: threshold alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, threshold alerts is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
