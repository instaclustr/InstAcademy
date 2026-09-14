---
source_id: "DOC-00633"
title: "Troubleshooting connector credential rotation"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > Troubleshooting connector credential rotation"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2024-07-01"
related_error_codes: ["ERR-2231"]
---

# Troubleshooting connector credential rotation

Connector Credential Rotation is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, connector credential rotation inherits group membership from your identity provider on each login.

When connector credential rotation is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, connector credential rotation is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
