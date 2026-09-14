---
source_id: "DOC-00429"
title: "How PDF export works"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > How PDF export works"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2026-04-07"
related_error_codes: ["ERR-1102"]
---

# How PDF export works

This page explains how PDF export works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, PDF export is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
