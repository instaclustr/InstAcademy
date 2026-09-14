---
source_id: "DOC-00541"
title: "How to configure anomaly alerts"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > How to configure anomaly alerts"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2026-04-08"
related_error_codes: ["ERR-4402"]
---

# How to configure anomaly alerts

This page explains how anomaly alerts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, anomaly alerts is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for anomaly alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: anomaly alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
