---
source_id: "DOC-00815"
title: "Connection Pooling settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > Connection Pooling settings reference"
product_area: "connectors"
product_version: "5.0"
acl: "professional"
updated_at: "2024-08-26"
related_error_codes: ["ERR-2288", "ERR-2231"]
---

# Connection Pooling settings reference

Connection Pooling lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, connection pooling is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for connection pooling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
