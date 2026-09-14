---
source_id: "DOC-00196"
title: "How embedded dashboards works"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > How embedded dashboards works"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2024-03-25"
related_error_codes: ["ERR-1210", "ERR-1102"]
---

# How embedded dashboards works

This page explains how embedded dashboards works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, embedded dashboards is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, embedded dashboards inherits group membership from your identity provider on each login.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
