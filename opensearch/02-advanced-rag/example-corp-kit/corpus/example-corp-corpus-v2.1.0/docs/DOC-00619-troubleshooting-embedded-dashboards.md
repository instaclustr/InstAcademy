---
source_id: "DOC-00619"
title: "Troubleshooting embedded dashboards"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > Troubleshooting embedded dashboards"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2024-02-27"
related_error_codes: ["ERR-1210", "ERR-1102"]
---

# Troubleshooting embedded dashboards

Embedded Dashboards lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, embedded dashboards is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, embedded dashboards inherits group membership from your identity provider on each login.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
