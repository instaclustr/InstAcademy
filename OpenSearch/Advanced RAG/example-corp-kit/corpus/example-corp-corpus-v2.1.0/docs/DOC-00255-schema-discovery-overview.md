---
source_id: "DOC-00255"
title: "Schema Discovery overview"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > Schema Discovery overview"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2024-02-09"
related_error_codes: ["ERR-2288", "ERR-2231"]
---

# Schema Discovery overview

This page explains how schema discovery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, schema discovery is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable schema discovery, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When schema discovery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
