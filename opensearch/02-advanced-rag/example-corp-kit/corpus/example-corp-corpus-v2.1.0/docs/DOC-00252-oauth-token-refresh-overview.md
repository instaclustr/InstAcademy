---
source_id: "DOC-00252"
title: "Oauth Token Refresh overview"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > Oauth Token Refresh overview"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2024-11-21"
related_error_codes: ["ERR-2231"]
---

# Oauth Token Refresh overview

This page explains how OAuth token refresh works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, OAuth token refresh inherits group membership from your identity provider on each login.

To enable OAuth token refresh, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
