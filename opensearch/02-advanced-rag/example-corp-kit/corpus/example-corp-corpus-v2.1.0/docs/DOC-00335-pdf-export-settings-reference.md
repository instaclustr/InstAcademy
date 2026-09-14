---
source_id: "DOC-00335"
title: "Pdf Export settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > Pdf Export settings reference"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2024-09-22"
related_error_codes: ["ERR-1210"]
---

# Pdf Export settings reference

Pdf Export is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

By default, PDF export is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
