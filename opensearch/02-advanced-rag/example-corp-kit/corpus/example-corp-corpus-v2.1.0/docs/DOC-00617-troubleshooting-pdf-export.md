---
source_id: "DOC-00617"
title: "Troubleshooting PDF export"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > Troubleshooting PDF export"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2025-06-12"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# Troubleshooting PDF export

Pdf Export lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

By default, PDF export is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
