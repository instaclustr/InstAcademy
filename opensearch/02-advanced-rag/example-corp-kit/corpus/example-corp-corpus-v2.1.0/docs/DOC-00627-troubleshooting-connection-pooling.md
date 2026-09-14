---
source_id: "DOC-00627"
title: "Troubleshooting connection pooling"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > Troubleshooting connection pooling"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2025-12-09"
related_error_codes: ["ERR-2209", "ERR-2231"]
---

# Troubleshooting connection pooling

Connection Pooling lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Audit events for connection pooling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, connection pooling is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
