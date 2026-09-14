---
source_id: "DOC-00680"
title: "How connector credential rotation works"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > How connector credential rotation works"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2025-11-29"
related_error_codes: ["ERR-2288", "ERR-2231"]
---

# How connector credential rotation works

Connector Credential Rotation is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When connector credential rotation is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, connector credential rotation inherits group membership from your identity provider on each login.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, connector credential rotation is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
