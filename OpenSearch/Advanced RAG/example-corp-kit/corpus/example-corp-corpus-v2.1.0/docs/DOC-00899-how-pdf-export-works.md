---
source_id: "DOC-00899"
title: "How PDF export works"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > How PDF export works"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2026-04-01"
related_error_codes: ["ERR-1210"]
---

# How PDF export works

This page explains how PDF export works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, PDF export is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
