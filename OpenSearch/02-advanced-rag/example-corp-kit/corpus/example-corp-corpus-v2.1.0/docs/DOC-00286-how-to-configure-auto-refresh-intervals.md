---
source_id: "DOC-00286"
title: "How to configure auto-refresh intervals"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > How to configure auto-refresh intervals"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2024-05-18"
related_error_codes: ["ERR-1210", "ERR-1102"]
---

# How to configure auto-refresh intervals

Auto-Refresh Intervals lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, auto-refresh intervals is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
