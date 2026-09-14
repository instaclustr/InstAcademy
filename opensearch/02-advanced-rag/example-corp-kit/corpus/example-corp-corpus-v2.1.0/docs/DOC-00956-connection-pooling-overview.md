---
source_id: "DOC-00956"
title: "Connection Pooling overview"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > Connection Pooling overview"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2026-01-18"
related_error_codes: ["ERR-2209", "ERR-2288"]
---

# Connection Pooling overview

Connection Pooling is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

By default, connection pooling is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
