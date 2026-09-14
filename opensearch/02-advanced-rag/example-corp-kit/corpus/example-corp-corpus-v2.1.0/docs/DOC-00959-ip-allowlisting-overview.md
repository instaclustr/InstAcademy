---
source_id: "DOC-00959"
title: "Ip Allowlisting overview"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > Ip Allowlisting overview"
product_area: "connectors"
product_version: "4.9"
acl: "enterprise"
updated_at: "2026-04-26"
related_error_codes: ["ERR-2231", "ERR-2288"]
---

# Ip Allowlisting overview

Ip Allowlisting lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

By default, IP allowlisting is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
