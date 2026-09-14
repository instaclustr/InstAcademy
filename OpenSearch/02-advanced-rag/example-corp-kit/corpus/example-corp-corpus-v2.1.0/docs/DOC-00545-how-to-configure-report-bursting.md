---
source_id: "DOC-00545"
title: "How to configure report bursting"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > How to configure report bursting"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2026-02-06"
related_error_codes: ["ERR-4402"]
---

# How to configure report bursting

Report Bursting lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Audit events for report bursting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, report bursting is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: report bursting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
