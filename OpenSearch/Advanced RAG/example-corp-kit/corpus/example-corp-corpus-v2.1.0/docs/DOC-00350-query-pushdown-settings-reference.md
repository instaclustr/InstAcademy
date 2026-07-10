---
source_id: "DOC-00350"
title: "Query Pushdown settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > Query Pushdown settings reference"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2024-03-29"
related_error_codes: ["ERR-2231", "ERR-2209"]
---

# Query Pushdown settings reference

Query Pushdown lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

By default, query pushdown is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable query pushdown, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

Audit events for query pushdown are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When query pushdown is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
