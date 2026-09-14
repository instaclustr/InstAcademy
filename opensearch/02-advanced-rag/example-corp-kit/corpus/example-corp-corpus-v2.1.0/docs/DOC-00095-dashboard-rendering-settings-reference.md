---
source_id: "DOC-00095"
title: "Dashboard Rendering settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > Dashboard Rendering settings reference"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2024-06-06"
related_error_codes: ["ERR-1147"]
---

# Dashboard Rendering settings reference

This page explains how dashboard rendering works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, dashboard rendering inherits group membership from your identity provider on each login.

By default, dashboard rendering is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
