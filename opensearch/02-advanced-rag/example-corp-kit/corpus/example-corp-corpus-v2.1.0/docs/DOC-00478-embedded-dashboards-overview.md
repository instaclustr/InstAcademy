---
source_id: "DOC-00478"
title: "Embedded Dashboards overview"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > Embedded Dashboards overview"
product_area: "dashboards"
product_version: "4.9"
acl: "professional"
updated_at: "2025-08-07"
related_error_codes: ["ERR-1102"]
---

# Embedded Dashboards overview

Embedded Dashboards lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, embedded dashboards is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, embedded dashboards inherits group membership from your identity provider on each login.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
