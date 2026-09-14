---
source_id: "DOC-00240"
title: "Dashboard Sharing overview"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > Dashboard Sharing overview"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2024-12-14"
related_error_codes: ["ERR-1147"]
---

# Dashboard Sharing overview

Dashboard Sharing is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, dashboard sharing inherits group membership from your identity provider on each login.

By default, dashboard sharing is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: dashboard sharing performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When dashboard sharing is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
