---
source_id: "DOC-00395"
title: "Troubleshooting IP allowlisting"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > Troubleshooting IP allowlisting"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2026-02-17"
related_error_codes: ["ERR-2231"]
---

# Troubleshooting IP allowlisting

This page explains how IP allowlisting works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, IP allowlisting is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
