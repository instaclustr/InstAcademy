---
source_id: "DOC-00628"
title: "Troubleshooting OAuth token refresh"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > Troubleshooting OAuth token refresh"
product_area: "connectors"
product_version: "4.8"
acl: "standard"
updated_at: "2025-10-22"
related_error_codes: ["ERR-2231", "ERR-2288"]
---

# Troubleshooting OAuth token refresh

Oauth Token Refresh lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable OAuth token refresh, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, OAuth token refresh inherits group membership from your identity provider on each login.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
