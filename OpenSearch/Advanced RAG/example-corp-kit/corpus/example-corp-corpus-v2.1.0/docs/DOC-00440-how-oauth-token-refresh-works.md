---
source_id: "DOC-00440"
title: "How OAuth token refresh works"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > How OAuth token refresh works"
product_area: "connectors"
product_version: "5.1"
acl: "standard"
updated_at: "2024-07-11"
related_error_codes: ["ERR-2231"]
---

# How OAuth token refresh works

Oauth Token Refresh is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, OAuth token refresh is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable OAuth token refresh, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, OAuth token refresh inherits group membership from your identity provider on each login.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
