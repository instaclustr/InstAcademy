---
source_id: "DOC-00988"
title: "How to configure dashboard rendering"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > How to configure dashboard rendering"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2025-12-11"
related_error_codes: ["ERR-1147"]
---

# How to configure dashboard rendering

This page explains how dashboard rendering works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, dashboard rendering is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

To enable dashboard rendering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
