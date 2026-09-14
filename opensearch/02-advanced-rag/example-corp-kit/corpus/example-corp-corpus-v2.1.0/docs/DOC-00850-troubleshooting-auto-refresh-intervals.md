---
source_id: "DOC-00850"
title: "Troubleshooting auto-refresh intervals"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > Troubleshooting auto-refresh intervals"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2026-01-17"
related_error_codes: ["ERR-1102"]
---

# Troubleshooting auto-refresh intervals

Auto-Refresh Intervals lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

By default, auto-refresh intervals is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
