---
source_id: "DOC-00613"
title: "Troubleshooting cross-filtering"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Troubleshooting cross-filtering"
product_area: "dashboards"
product_version: "5.1"
acl: "enterprise"
updated_at: "2025-06-12"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# Troubleshooting cross-filtering

Cross-Filtering lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
