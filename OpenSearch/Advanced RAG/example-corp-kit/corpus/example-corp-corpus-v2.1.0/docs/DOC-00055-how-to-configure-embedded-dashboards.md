---
source_id: "DOC-00055"
title: "How to configure embedded dashboards"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > How to configure embedded dashboards"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2024-11-06"
related_error_codes: ["ERR-1147"]
---

# How to configure embedded dashboards

This page explains how embedded dashboards works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for embedded dashboards are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, embedded dashboards is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, embedded dashboards inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
