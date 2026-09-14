---
source_id: "DOC-00070"
title: "How to configure threshold alerts"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > How to configure threshold alerts"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2025-01-26"
related_error_codes: ["ERR-4402"]
---

# How to configure threshold alerts

Threshold Alerts lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, threshold alerts is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for threshold alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: threshold alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, threshold alerts inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
