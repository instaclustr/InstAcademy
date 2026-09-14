---
source_id: "DOC-00299"
title: "How to configure OAuth token refresh"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > How to configure OAuth token refresh"
product_area: "connectors"
product_version: "4.8"
acl: "standard"
updated_at: "2025-02-19"
related_error_codes: ["ERR-2231"]
---

# How to configure OAuth token refresh

Oauth Token Refresh lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

By default, OAuth token refresh is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, OAuth token refresh inherits group membership from your identity provider on each login.

To enable OAuth token refresh, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
