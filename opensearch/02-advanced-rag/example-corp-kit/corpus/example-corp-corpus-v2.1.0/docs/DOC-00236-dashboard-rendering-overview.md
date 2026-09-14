---
source_id: "DOC-00236"
title: "Dashboard Rendering overview"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > Dashboard Rendering overview"
product_area: "dashboards"
product_version: "5.0"
acl: "professional"
updated_at: "2024-04-27"
related_error_codes: ["ERR-1102"]
---

# Dashboard Rendering overview

Dashboard Rendering lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

To enable dashboard rendering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, dashboard rendering is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
