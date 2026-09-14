---
source_id: "DOC-00913"
title: "How schema discovery works"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > How schema discovery works"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2025-11-11"
related_error_codes: ["ERR-2231", "ERR-2209"]
---

# How schema discovery works

Schema Discovery is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable schema discovery, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

By default, schema discovery is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When schema discovery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
