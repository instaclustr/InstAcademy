---
source_id: "DOC-00770"
title: "How to configure SSH tunneling"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > How to configure SSH tunneling"
product_area: "connectors"
product_version: "5.0"
acl: "professional"
updated_at: "2025-02-02"
related_error_codes: ["ERR-2231", "ERR-2209"]
---

# How to configure SSH tunneling

Ssh Tunneling lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, SSH tunneling is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
