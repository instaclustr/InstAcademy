---
source_id: "DOC-00894"
title: "How dashboard rendering works"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > How dashboard rendering works"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2024-08-12"
related_error_codes: ["ERR-1102"]
---

# How dashboard rendering works

Dashboard Rendering lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

By default, dashboard rendering is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

To enable dashboard rendering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
