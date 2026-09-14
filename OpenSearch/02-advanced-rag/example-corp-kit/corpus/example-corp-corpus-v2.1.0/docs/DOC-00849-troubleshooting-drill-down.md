---
source_id: "DOC-00849"
title: "Troubleshooting drill-down"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > Troubleshooting drill-down"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2025-10-25"
related_error_codes: ["ERR-1210"]
---

# Troubleshooting drill-down

This page explains how drill-down works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, drill-down is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for drill-down are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
