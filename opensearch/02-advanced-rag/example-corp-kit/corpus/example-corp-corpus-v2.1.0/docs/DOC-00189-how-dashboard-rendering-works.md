---
source_id: "DOC-00189"
title: "How dashboard rendering works"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > How dashboard rendering works"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-03-31"
related_error_codes: ["ERR-1147", "ERR-1102"]
---

# How dashboard rendering works

Dashboard Rendering is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, dashboard rendering is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable dashboard rendering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
