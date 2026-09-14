---
source_id: "DOC-00471"
title: "Dashboard Rendering overview"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > Dashboard Rendering overview"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2026-03-27"
related_error_codes: ["ERR-1210"]
---

# Dashboard Rendering overview

Dashboard Rendering lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, dashboard rendering is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
