---
source_id: "DOC-00142"
title: "Troubleshooting dashboard rendering"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > Troubleshooting dashboard rendering"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-09-17"
related_error_codes: ["ERR-1210"]
---

# Troubleshooting dashboard rendering

Dashboard Rendering lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

By default, dashboard rendering is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
