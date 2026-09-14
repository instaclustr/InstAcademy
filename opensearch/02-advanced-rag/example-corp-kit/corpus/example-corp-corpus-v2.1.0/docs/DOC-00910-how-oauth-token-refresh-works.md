---
source_id: "DOC-00910"
title: "How OAuth token refresh works"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > How OAuth token refresh works"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2025-09-16"
related_error_codes: ["ERR-2231"]
---

# How OAuth token refresh works

Oauth Token Refresh lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, OAuth token refresh inherits group membership from your identity provider on each login.

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable OAuth token refresh, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
