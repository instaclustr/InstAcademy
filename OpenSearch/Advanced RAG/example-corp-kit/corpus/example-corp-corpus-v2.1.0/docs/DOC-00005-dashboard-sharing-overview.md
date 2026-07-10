---
source_id: "DOC-00005"
title: "Dashboard Sharing overview"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > Dashboard Sharing overview"
product_area: "dashboards"
product_version: "4.8"
acl: "professional"
updated_at: "2025-11-26"
related_error_codes: ["ERR-1147", "ERR-1102"]
---

# Dashboard Sharing overview

Dashboard Sharing is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, dashboard sharing is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: dashboard sharing performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When dashboard sharing is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, dashboard sharing inherits group membership from your identity provider on each login.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
