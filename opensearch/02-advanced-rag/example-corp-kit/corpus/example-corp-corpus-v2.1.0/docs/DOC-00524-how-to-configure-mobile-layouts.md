---
source_id: "DOC-00524"
title: "How to configure mobile layouts"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > How to configure mobile layouts"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2025-08-06"
related_error_codes: ["ERR-1102"]
---

# How to configure mobile layouts

Mobile Layouts is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, mobile layouts is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for mobile layouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, mobile layouts inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
