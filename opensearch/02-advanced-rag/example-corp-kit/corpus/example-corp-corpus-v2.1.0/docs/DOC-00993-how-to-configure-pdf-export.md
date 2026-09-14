---
source_id: "DOC-00993"
title: "How to configure PDF export"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > How to configure PDF export"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2024-05-13"
related_error_codes: ["ERR-1147"]
---

# How to configure PDF export

Pdf Export is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
