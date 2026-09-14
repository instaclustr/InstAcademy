---
source_id: "DOC-00523"
title: "How to configure PDF export"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > How to configure PDF export"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2024-02-09"
related_error_codes: ["ERR-1210", "ERR-1102"]
---

# How to configure PDF export

Pdf Export lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, PDF export is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
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
