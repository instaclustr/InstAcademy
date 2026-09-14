---
source_id: "DOC-00522"
title: "How to configure dashboard sharing"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > How to configure dashboard sharing"
product_area: "dashboards"
product_version: "4.9"
acl: "enterprise"
updated_at: "2025-07-05"
related_error_codes: ["ERR-1102", "ERR-1210"]
---

# How to configure dashboard sharing

Dashboard Sharing is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When dashboard sharing is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dashboard sharing performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, dashboard sharing is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, dashboard sharing inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
