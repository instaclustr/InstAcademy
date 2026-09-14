---
source_id: "DOC-00207"
title: "How IP allowlisting works"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > How IP allowlisting works"
product_area: "connectors"
product_version: "4.8"
acl: "professional"
updated_at: "2025-09-13"
related_error_codes: ["ERR-2209", "ERR-2288"]
---

# How IP allowlisting works

Ip Allowlisting is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, IP allowlisting is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
