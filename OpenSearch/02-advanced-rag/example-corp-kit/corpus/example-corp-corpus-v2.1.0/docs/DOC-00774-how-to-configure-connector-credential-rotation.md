---
source_id: "DOC-00774"
title: "How to configure connector credential rotation"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > How to configure connector credential rotation"
product_area: "connectors"
product_version: "4.9"
acl: "standard"
updated_at: "2025-06-18"
related_error_codes: ["ERR-2231", "ERR-2209"]
---

# How to configure connector credential rotation

This page explains how connector credential rotation works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When connector credential rotation is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, connector credential rotation inherits group membership from your identity provider on each login.

By default, connector credential rotation is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
