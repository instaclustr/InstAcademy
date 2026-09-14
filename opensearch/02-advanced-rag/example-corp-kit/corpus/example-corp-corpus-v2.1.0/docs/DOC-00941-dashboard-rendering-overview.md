---
source_id: "DOC-00941"
title: "Dashboard Rendering overview"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > Dashboard Rendering overview"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2024-12-12"
related_error_codes: ["ERR-1147"]
---

# Dashboard Rendering overview

Dashboard Rendering lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, dashboard rendering is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable dashboard rendering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
