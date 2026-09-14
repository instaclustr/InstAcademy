---
source_id: "DOC-00805"
title: "Pdf Export settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > Pdf Export settings reference"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2025-12-14"
related_error_codes: ["ERR-1147", "ERR-1102"]
---

# Pdf Export settings reference

Pdf Export is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, PDF export is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
