---
source_id: "DOC-00662"
title: "How auto-refresh intervals works"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > How auto-refresh intervals works"
product_area: "dashboards"
product_version: "4.9"
acl: "enterprise"
updated_at: "2024-11-11"
related_error_codes: ["ERR-1102"]
---

# How auto-refresh intervals works

This page explains how auto-refresh intervals works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
