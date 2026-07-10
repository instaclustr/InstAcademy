---
source_id: "DOC-00474"
title: "Auto-Refresh Intervals overview"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > Auto-Refresh Intervals overview"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2026-01-08"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# Auto-Refresh Intervals overview

Auto-Refresh Intervals lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

By default, auto-refresh intervals is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
