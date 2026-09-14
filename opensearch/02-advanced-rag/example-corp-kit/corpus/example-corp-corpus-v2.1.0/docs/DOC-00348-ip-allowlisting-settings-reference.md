---
source_id: "DOC-00348"
title: "Ip Allowlisting settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > Ip Allowlisting settings reference"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2025-01-24"
related_error_codes: ["ERR-2231", "ERR-2288"]
---

# Ip Allowlisting settings reference

This page explains how IP allowlisting works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, IP allowlisting is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
