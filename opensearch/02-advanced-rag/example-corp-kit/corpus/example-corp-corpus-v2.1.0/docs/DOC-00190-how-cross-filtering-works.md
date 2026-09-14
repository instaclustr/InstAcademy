---
source_id: "DOC-00190"
title: "How cross-filtering works"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > How cross-filtering works"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2024-09-01"
related_error_codes: ["ERR-1210"]
---

# How cross-filtering works

This page explains how cross-filtering works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

By default, cross-filtering is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
