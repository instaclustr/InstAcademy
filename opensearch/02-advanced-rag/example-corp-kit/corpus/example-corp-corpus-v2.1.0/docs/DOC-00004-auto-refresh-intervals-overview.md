---
source_id: "DOC-00004"
title: "Auto-Refresh Intervals overview"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > Auto-Refresh Intervals overview"
product_area: "dashboards"
product_version: "5.0"
acl: "enterprise"
updated_at: "2025-11-28"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# Auto-Refresh Intervals overview

This page explains how auto-refresh intervals works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, auto-refresh intervals is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
