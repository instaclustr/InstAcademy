---
source_id: "DOC-00957"
title: "Oauth Token Refresh overview"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > Oauth Token Refresh overview"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2024-01-27"
related_error_codes: ["ERR-2288", "ERR-2209"]
---

# Oauth Token Refresh overview

Oauth Token Refresh lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

By default, OAuth token refresh is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, OAuth token refresh inherits group membership from your identity provider on each login.

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
