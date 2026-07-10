---
source_id: "DOC-00208"
title: "How schema discovery works"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > How schema discovery works"
product_area: "connectors"
product_version: "5.1"
acl: "professional"
updated_at: "2024-09-01"
related_error_codes: ["ERR-2231", "ERR-2288"]
---

# How schema discovery works

This page explains how schema discovery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: schema discovery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When schema discovery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

By default, schema discovery is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
