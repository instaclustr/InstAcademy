---
source_id: "DOC-00066"
title: "How to configure IP allowlisting"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > How to configure IP allowlisting"
product_area: "connectors"
product_version: "5.0"
acl: "enterprise"
updated_at: "2024-06-16"
related_error_codes: ["ERR-2209", "ERR-2231"]
---

# How to configure IP allowlisting

Ip Allowlisting lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, IP allowlisting is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
