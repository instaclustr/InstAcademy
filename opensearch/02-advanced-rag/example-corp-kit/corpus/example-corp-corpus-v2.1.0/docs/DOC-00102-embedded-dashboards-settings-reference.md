---
source_id: "DOC-00102"
title: "Embedded Dashboards settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > Embedded Dashboards settings reference"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2025-08-27"
related_error_codes: ["ERR-1210", "ERR-1102"]
---

# Embedded Dashboards settings reference

Embedded Dashboards lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Audit events for embedded dashboards are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, embedded dashboards is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, embedded dashboards inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
