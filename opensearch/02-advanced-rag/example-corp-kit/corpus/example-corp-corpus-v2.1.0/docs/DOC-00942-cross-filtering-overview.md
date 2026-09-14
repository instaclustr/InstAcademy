---
source_id: "DOC-00942"
title: "Cross-Filtering overview"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Cross-Filtering overview"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2024-08-13"
related_error_codes: ["ERR-1210", "ERR-1147"]
---

# Cross-Filtering overview

Cross-Filtering lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

By default, cross-filtering is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
