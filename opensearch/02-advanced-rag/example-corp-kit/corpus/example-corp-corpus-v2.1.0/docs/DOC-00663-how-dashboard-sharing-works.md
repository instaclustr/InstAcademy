---
source_id: "DOC-00663"
title: "How dashboard sharing works"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > How dashboard sharing works"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2024-06-26"
related_error_codes: ["ERR-1102"]
---

# How dashboard sharing works

This page explains how dashboard sharing works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, dashboard sharing inherits group membership from your identity provider on each login.

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, dashboard sharing is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: dashboard sharing performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable dashboard sharing, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
