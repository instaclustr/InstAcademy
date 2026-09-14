---
source_id: "DOC-00398"
title: "Troubleshooting connector credential rotation"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > Troubleshooting connector credential rotation"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2026-04-13"
related_error_codes: ["ERR-2209", "ERR-2231"]
---

# Troubleshooting connector credential rotation

Connector Credential Rotation is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: connector credential rotation performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, connector credential rotation inherits group membership from your identity provider on each login.

By default, connector credential rotation is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
