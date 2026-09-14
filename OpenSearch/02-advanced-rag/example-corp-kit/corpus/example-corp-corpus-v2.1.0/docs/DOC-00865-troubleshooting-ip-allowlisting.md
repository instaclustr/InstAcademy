---
source_id: "DOC-00865"
title: "Troubleshooting IP allowlisting"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > Troubleshooting IP allowlisting"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2025-12-09"
related_error_codes: ["ERR-2231", "ERR-2288"]
---

# Troubleshooting IP allowlisting

This page explains how IP allowlisting works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, IP allowlisting is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
