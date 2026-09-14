---
source_id: "DOC-00381"
title: "Troubleshooting dashboard sharing"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > Troubleshooting dashboard sharing"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2025-07-29"
related_error_codes: ["ERR-1102", "ERR-1210"]
---

# Troubleshooting dashboard sharing

Dashboard Sharing lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

To enable dashboard sharing, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: dashboard sharing performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, dashboard sharing is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, dashboard sharing inherits group membership from your identity provider on each login.

When dashboard sharing is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
