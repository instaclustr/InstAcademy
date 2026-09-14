---
source_id: "DOC-00754"
title: "How to configure cross-filtering"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > How to configure cross-filtering"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2024-11-03"
related_error_codes: ["ERR-1210"]
---

# How to configure cross-filtering

Cross-Filtering is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

By default, cross-filtering is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
