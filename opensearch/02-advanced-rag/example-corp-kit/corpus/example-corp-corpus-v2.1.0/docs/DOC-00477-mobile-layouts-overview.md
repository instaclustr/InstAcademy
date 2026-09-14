---
source_id: "DOC-00477"
title: "Mobile Layouts overview"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > Mobile Layouts overview"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2025-05-20"
related_error_codes: ["ERR-1210"]
---

# Mobile Layouts overview

Mobile Layouts lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, mobile layouts inherits group membership from your identity provider on each login.

By default, mobile layouts is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
