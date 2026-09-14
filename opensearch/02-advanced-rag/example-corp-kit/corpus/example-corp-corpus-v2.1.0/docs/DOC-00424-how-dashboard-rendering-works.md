---
source_id: "DOC-00424"
title: "How dashboard rendering works"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > How dashboard rendering works"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2026-02-02"
related_error_codes: ["ERR-1210", "ERR-1102"]
---

# How dashboard rendering works

Dashboard Rendering lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, dashboard rendering is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
