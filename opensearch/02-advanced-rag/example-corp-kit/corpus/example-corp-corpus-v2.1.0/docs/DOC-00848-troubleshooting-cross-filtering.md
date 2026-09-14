---
source_id: "DOC-00848"
title: "Troubleshooting cross-filtering"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Troubleshooting cross-filtering"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2025-10-05"
related_error_codes: ["ERR-1147"]
---

# Troubleshooting cross-filtering

Cross-Filtering lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

By default, cross-filtering is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
