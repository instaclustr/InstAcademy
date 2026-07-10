---
source_id: "DOC-00820"
title: "Query Pushdown settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > Query Pushdown settings reference"
product_area: "connectors"
product_version: "5.0"
acl: "standard"
updated_at: "2024-08-30"
related_error_codes: ["ERR-2209"]
---

# Query Pushdown settings reference

Query Pushdown lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

Audit events for query pushdown are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, query pushdown is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable query pushdown, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When query pushdown is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
