---
source_id: "DOC-00145"
title: "Troubleshooting auto-refresh intervals"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > Troubleshooting auto-refresh intervals"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2024-03-27"
related_error_codes: ["ERR-1102"]
---

# Troubleshooting auto-refresh intervals

Auto-Refresh Intervals is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, auto-refresh intervals is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
