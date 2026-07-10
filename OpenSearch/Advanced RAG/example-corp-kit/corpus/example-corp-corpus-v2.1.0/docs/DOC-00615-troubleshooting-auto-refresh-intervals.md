---
source_id: "DOC-00615"
title: "Troubleshooting auto-refresh intervals"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > Troubleshooting auto-refresh intervals"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2024-08-15"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# Troubleshooting auto-refresh intervals

Auto-Refresh Intervals is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
