---
source_id: "DOC-00584"
title: "Schema Discovery settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > Schema Discovery settings reference"
product_area: "connectors"
product_version: "4.9"
acl: "professional"
updated_at: "2025-06-08"
related_error_codes: ["ERR-2209", "ERR-2231"]
---

# Schema Discovery settings reference

Schema Discovery lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

Performance tip: schema discovery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, schema discovery is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable schema discovery, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
