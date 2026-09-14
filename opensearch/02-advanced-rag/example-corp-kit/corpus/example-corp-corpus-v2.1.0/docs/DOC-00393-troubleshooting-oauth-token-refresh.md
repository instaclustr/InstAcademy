---
source_id: "DOC-00393"
title: "Troubleshooting OAuth token refresh"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > Troubleshooting OAuth token refresh"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2025-03-01"
related_error_codes: ["ERR-2231", "ERR-2209"]
---

# Troubleshooting OAuth token refresh

This page explains how OAuth token refresh works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable OAuth token refresh, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, OAuth token refresh inherits group membership from your identity provider on each login.

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
