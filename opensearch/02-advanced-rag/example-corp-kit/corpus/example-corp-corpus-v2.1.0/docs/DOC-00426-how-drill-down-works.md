---
source_id: "DOC-00426"
title: "How drill-down works"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > How drill-down works"
product_area: "dashboards"
product_version: "5.1"
acl: "standard"
updated_at: "2026-04-18"
related_error_codes: ["ERR-1147", "ERR-1102"]
---

# How drill-down works

Drill-Down is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, drill-down is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
