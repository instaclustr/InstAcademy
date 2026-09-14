---
source_id: "DOC-00710"
title: "Dashboard Sharing overview"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > Dashboard Sharing overview"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2025-06-25"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# Dashboard Sharing overview

Dashboard Sharing lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

When dashboard sharing is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable dashboard sharing, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, dashboard sharing inherits group membership from your identity provider on each login.

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: dashboard sharing performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
