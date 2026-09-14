---
source_id: "DOC-00473"
title: "Drill-Down overview"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > Drill-Down overview"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-09-06"
related_error_codes: ["ERR-1147"]
---

# Drill-Down overview

Drill-Down is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, drill-down is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
