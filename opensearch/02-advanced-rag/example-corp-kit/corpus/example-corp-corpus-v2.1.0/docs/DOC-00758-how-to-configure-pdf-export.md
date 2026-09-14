---
source_id: "DOC-00758"
title: "How to configure PDF export"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > How to configure PDF export"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2025-06-02"
related_error_codes: ["ERR-1210"]
---

# How to configure PDF export

Pdf Export is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

By default, PDF export is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
