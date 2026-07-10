---
source_id: "DOC-00380"
title: "Troubleshooting auto-refresh intervals"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > Troubleshooting auto-refresh intervals"
product_area: "dashboards"
product_version: "4.9"
acl: "standard"
updated_at: "2025-01-27"
related_error_codes: ["ERR-1210", "ERR-1147"]
---

# Troubleshooting auto-refresh intervals

Auto-Refresh Intervals lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, auto-refresh intervals is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
