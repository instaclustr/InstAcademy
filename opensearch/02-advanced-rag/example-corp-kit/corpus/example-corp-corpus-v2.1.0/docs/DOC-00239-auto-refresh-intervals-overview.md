---
source_id: "DOC-00239"
title: "Auto-Refresh Intervals overview"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > Auto-Refresh Intervals overview"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2026-03-19"
related_error_codes: ["ERR-1102", "ERR-1210"]
---

# Auto-Refresh Intervals overview

Auto-Refresh Intervals is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, auto-refresh intervals is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
