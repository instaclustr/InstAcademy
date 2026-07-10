---
source_id: "DOC-00678"
title: "How schema discovery works"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > How schema discovery works"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2024-09-11"
related_error_codes: ["ERR-2231"]
---

# How schema discovery works

Schema Discovery is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable schema discovery, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, schema discovery is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: schema discovery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
