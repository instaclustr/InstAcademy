---
source_id: "DOC-00567"
title: "Drill-Down settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > Drill-Down settings reference"
product_area: "dashboards"
product_version: "5.0"
acl: "enterprise"
updated_at: "2024-11-02"
related_error_codes: ["ERR-1147"]
---

# Drill-Down settings reference

Drill-Down lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, drill-down is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for drill-down are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
