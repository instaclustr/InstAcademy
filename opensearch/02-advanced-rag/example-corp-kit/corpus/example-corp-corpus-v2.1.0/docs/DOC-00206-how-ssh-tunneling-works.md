---
source_id: "DOC-00206"
title: "How SSH tunneling works"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > How SSH tunneling works"
product_area: "connectors"
product_version: "4.8"
acl: "enterprise"
updated_at: "2024-04-28"
related_error_codes: ["ERR-2231", "ERR-2209"]
---

# How SSH tunneling works

Ssh Tunneling is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for SSH tunneling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, SSH tunneling is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
