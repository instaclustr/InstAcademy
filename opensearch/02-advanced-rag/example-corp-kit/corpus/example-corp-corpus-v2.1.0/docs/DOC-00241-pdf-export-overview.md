---
source_id: "DOC-00241"
title: "Pdf Export overview"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > Pdf Export overview"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-06-27"
related_error_codes: ["ERR-1210", "ERR-1102"]
---

# Pdf Export overview

This page explains how PDF export works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
