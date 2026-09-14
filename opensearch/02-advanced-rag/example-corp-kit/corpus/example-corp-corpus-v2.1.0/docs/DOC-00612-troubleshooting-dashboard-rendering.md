---
source_id: "DOC-00612"
title: "Troubleshooting dashboard rendering"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > Troubleshooting dashboard rendering"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2024-08-24"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# Troubleshooting dashboard rendering

Dashboard Rendering is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable dashboard rendering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
