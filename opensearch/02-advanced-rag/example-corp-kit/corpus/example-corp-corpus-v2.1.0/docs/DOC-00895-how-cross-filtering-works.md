---
source_id: "DOC-00895"
title: "How cross-filtering works"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > How cross-filtering works"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2024-02-19"
related_error_codes: ["ERR-1210", "ERR-1102"]
---

# How cross-filtering works

Cross-Filtering lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, cross-filtering is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
