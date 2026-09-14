---
source_id: "DOC-00800"
title: "Dashboard Rendering settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > Dashboard Rendering settings reference"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2026-03-29"
related_error_codes: ["ERR-1147", "ERR-1102"]
---

# Dashboard Rendering settings reference

Dashboard Rendering lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

By default, dashboard rendering is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
