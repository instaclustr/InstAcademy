---
source_id: "DOC-00946"
title: "Pdf Export overview"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > Pdf Export overview"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2025-03-08"
related_error_codes: ["ERR-1102"]
---

# Pdf Export overview

Pdf Export lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, PDF export is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
