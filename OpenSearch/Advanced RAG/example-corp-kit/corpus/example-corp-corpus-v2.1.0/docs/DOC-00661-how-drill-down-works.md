---
source_id: "DOC-00661"
title: "How drill-down works"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > How drill-down works"
product_area: "dashboards"
product_version: "5.0"
acl: "standard"
updated_at: "2024-01-30"
related_error_codes: ["ERR-1210", "ERR-1102"]
---

# How drill-down works

Drill-Down lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

By default, drill-down is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

Audit events for drill-down are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
