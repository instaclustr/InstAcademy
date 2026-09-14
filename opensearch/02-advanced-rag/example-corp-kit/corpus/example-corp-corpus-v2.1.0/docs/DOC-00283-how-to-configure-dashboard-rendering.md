---
source_id: "DOC-00283"
title: "How to configure dashboard rendering"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > How to configure dashboard rendering"
product_area: "dashboards"
product_version: "4.9"
acl: "enterprise"
updated_at: "2025-03-04"
related_error_codes: ["ERR-1210", "ERR-1147"]
---

# How to configure dashboard rendering

Dashboard Rendering is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

To enable dashboard rendering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
