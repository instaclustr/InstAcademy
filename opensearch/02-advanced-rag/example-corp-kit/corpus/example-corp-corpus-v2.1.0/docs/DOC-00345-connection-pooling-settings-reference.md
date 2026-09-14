---
source_id: "DOC-00345"
title: "Connection Pooling settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > Connection Pooling settings reference"
product_area: "connectors"
product_version: "4.8"
acl: "professional"
updated_at: "2024-12-17"
related_error_codes: ["ERR-2231"]
---

# Connection Pooling settings reference

This page explains how connection pooling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, connection pooling is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
