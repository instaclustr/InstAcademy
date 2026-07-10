---
source_id: "DOC-00001"
title: "Dashboard Rendering overview"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > Dashboard Rendering overview"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2026-06-05"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# Dashboard Rendering overview

Dashboard Rendering lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

By default, dashboard rendering is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable dashboard rendering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
