---
source_id: "DOC-00332"
title: "Drill-Down settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > Drill-Down settings reference"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2025-05-10"
related_error_codes: ["ERR-1210", "ERR-1147"]
---

# Drill-Down settings reference

Drill-Down is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, drill-down is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
