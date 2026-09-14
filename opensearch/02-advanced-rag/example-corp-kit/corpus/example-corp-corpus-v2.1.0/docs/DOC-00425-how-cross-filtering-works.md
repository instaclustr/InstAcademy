---
source_id: "DOC-00425"
title: "How cross-filtering works"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > How cross-filtering works"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2025-09-05"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# How cross-filtering works

Cross-Filtering lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

By default, cross-filtering is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
