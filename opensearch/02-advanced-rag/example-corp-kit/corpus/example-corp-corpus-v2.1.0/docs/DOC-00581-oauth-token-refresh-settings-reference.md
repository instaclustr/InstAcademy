---
source_id: "DOC-00581"
title: "Oauth Token Refresh settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > Oauth Token Refresh settings reference"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2024-10-19"
related_error_codes: ["ERR-2209", "ERR-2288"]
---

# Oauth Token Refresh settings reference

Oauth Token Refresh lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, OAuth token refresh inherits group membership from your identity provider on each login.

To enable OAuth token refresh, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, OAuth token refresh is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
