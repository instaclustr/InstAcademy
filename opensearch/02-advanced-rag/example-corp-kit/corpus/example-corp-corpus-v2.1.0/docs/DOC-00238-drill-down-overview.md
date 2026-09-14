---
source_id: "DOC-00238"
title: "Drill-Down overview"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > Drill-Down overview"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2024-08-28"
related_error_codes: ["ERR-1102"]
---

# Drill-Down overview

Drill-Down lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, drill-down is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
