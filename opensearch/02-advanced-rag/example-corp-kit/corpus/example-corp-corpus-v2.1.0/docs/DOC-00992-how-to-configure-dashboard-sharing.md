---
source_id: "DOC-00992"
title: "How to configure dashboard sharing"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > How to configure dashboard sharing"
product_area: "dashboards"
product_version: "5.1"
acl: "professional"
updated_at: "2024-05-28"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# How to configure dashboard sharing

This page explains how dashboard sharing works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, dashboard sharing inherits group membership from your identity provider on each login.

To enable dashboard sharing, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: dashboard sharing performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, dashboard sharing is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
