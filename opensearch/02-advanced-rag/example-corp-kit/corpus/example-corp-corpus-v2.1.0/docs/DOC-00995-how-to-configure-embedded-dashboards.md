---
source_id: "DOC-00995"
title: "How to configure embedded dashboards"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > How to configure embedded dashboards"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2024-05-25"
related_error_codes: ["ERR-1102", "ERR-1210"]
---

# How to configure embedded dashboards

Embedded Dashboards is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, embedded dashboards is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, embedded dashboards inherits group membership from your identity provider on each login.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
