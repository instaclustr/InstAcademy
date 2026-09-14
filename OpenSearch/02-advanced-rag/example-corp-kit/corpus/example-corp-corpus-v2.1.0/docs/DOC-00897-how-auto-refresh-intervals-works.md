---
source_id: "DOC-00897"
title: "How auto-refresh intervals works"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > How auto-refresh intervals works"
product_area: "dashboards"
product_version: "5.1"
acl: "standard"
updated_at: "2024-12-08"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# How auto-refresh intervals works

Auto-Refresh Intervals lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, auto-refresh intervals is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
