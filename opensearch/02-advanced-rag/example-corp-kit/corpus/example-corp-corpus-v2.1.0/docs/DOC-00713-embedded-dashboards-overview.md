---
source_id: "DOC-00713"
title: "Embedded Dashboards overview"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > Embedded Dashboards overview"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2025-11-24"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# Embedded Dashboards overview

Embedded Dashboards lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, embedded dashboards inherits group membership from your identity provider on each login.

Audit events for embedded dashboards are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, embedded dashboards is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
