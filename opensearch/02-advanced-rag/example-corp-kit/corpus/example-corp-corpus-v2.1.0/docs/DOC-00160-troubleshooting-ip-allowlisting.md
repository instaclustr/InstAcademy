---
source_id: "DOC-00160"
title: "Troubleshooting IP allowlisting"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > Troubleshooting IP allowlisting"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2026-05-28"
related_error_codes: ["ERR-2231"]
---

# Troubleshooting IP allowlisting

Ip Allowlisting lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

By default, IP allowlisting is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
