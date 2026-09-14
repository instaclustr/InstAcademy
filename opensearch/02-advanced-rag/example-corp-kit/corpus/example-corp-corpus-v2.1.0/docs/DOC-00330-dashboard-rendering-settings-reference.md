---
source_id: "DOC-00330"
title: "Dashboard Rendering settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > Dashboard Rendering settings reference"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2025-01-12"
related_error_codes: ["ERR-1102"]
---

# Dashboard Rendering settings reference

This page explains how dashboard rendering works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, dashboard rendering is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
