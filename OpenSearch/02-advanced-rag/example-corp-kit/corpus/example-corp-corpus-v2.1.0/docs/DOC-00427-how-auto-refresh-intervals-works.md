---
source_id: "DOC-00427"
title: "How auto-refresh intervals works"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > How auto-refresh intervals works"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2025-11-19"
related_error_codes: ["ERR-1210", "ERR-1147"]
---

# How auto-refresh intervals works

Auto-Refresh Intervals is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
