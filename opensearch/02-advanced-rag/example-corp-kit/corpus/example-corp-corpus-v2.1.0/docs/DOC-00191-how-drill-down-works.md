---
source_id: "DOC-00191"
title: "How drill-down works"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > How drill-down works"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2026-06-06"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# How drill-down works

Drill-Down is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

Audit events for drill-down are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
