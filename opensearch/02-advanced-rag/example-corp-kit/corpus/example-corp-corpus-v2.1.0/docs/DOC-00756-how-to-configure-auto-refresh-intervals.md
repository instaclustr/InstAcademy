---
source_id: "DOC-00756"
title: "How to configure auto-refresh intervals"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > How to configure auto-refresh intervals"
product_area: "dashboards"
product_version: "5.0"
acl: "enterprise"
updated_at: "2025-12-20"
related_error_codes: ["ERR-1147"]
---

# How to configure auto-refresh intervals

Auto-Refresh Intervals is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, auto-refresh intervals inherits group membership from your identity provider on each login.

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, auto-refresh intervals is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
