---
source_id: "DOC-00801"
title: "Cross-Filtering settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Cross-Filtering settings reference"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2025-01-29"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# Cross-Filtering settings reference

Cross-Filtering is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, cross-filtering is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
