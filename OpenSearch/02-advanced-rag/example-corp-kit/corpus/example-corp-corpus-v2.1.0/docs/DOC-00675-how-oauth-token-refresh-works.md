---
source_id: "DOC-00675"
title: "How OAuth token refresh works"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > How OAuth token refresh works"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2024-04-27"
related_error_codes: ["ERR-2231"]
---

# How OAuth token refresh works

This page explains how OAuth token refresh works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, OAuth token refresh is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, OAuth token refresh inherits group membership from your identity provider on each login.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
