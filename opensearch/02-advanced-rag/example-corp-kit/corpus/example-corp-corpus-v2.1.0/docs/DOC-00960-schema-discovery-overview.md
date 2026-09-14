---
source_id: "DOC-00960"
title: "Schema Discovery overview"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > Schema Discovery overview"
product_area: "connectors"
product_version: "4.8"
acl: "professional"
updated_at: "2026-03-16"
related_error_codes: ["ERR-2209", "ERR-2231"]
---

# Schema Discovery overview

Schema Discovery lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

When schema discovery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

To enable schema discovery, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, schema discovery is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
