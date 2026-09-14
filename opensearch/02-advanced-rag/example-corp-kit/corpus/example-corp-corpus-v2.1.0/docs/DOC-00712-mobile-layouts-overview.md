---
source_id: "DOC-00712"
title: "Mobile Layouts overview"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > Mobile Layouts overview"
product_area: "dashboards"
product_version: "4.8"
acl: "professional"
updated_at: "2024-11-23"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# Mobile Layouts overview

This page explains how mobile layouts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, mobile layouts inherits group membership from your identity provider on each login.

By default, mobile layouts is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for mobile layouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
