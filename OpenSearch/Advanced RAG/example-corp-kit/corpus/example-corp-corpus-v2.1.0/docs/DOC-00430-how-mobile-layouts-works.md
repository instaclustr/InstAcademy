---
source_id: "DOC-00430"
title: "How mobile layouts works"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > How mobile layouts works"
product_area: "dashboards"
product_version: "5.0"
acl: "standard"
updated_at: "2026-04-26"
related_error_codes: ["ERR-1102"]
---

# How mobile layouts works

Mobile Layouts lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, mobile layouts inherits group membership from your identity provider on each login.

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, mobile layouts is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
