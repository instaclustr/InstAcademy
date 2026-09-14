---
source_id: "DOC-00866"
title: "Troubleshooting schema discovery"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > Troubleshooting schema discovery"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2026-04-16"
related_error_codes: ["ERR-2288", "ERR-2231"]
---

# Troubleshooting schema discovery

Schema Discovery is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When schema discovery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

To enable schema discovery, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: schema discovery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
