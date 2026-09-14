---
source_id: "DOC-00475"
title: "Dashboard Sharing overview"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > Dashboard Sharing overview"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-05-16"
related_error_codes: ["ERR-1210"]
---

# Dashboard Sharing overview

Dashboard Sharing is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, dashboard sharing is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: dashboard sharing performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When dashboard sharing is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, dashboard sharing inherits group membership from your identity provider on each login.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
