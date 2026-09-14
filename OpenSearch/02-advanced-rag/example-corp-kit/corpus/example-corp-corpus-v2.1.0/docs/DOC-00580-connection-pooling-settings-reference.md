---
source_id: "DOC-00580"
title: "Connection Pooling settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > Connection Pooling settings reference"
product_area: "connectors"
product_version: "5.0"
acl: "enterprise"
updated_at: "2024-06-22"
related_error_codes: ["ERR-2231"]
---

# Connection Pooling settings reference

Connection Pooling is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, connection pooling is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
