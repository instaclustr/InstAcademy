---
source_id: "DOC-00803"
title: "Auto-Refresh Intervals settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > Auto-Refresh Intervals settings reference"
product_area: "dashboards"
product_version: "4.9"
acl: "standard"
updated_at: "2024-07-31"
related_error_codes: ["ERR-1147"]
---

# Auto-Refresh Intervals settings reference

Auto-Refresh Intervals is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, auto-refresh intervals is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
