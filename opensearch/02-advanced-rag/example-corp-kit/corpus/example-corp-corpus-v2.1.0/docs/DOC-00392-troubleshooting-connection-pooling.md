---
source_id: "DOC-00392"
title: "Troubleshooting connection pooling"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > Troubleshooting connection pooling"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2024-07-28"
related_error_codes: ["ERR-2209", "ERR-2231"]
---

# Troubleshooting connection pooling

Connection Pooling is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for connection pooling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
