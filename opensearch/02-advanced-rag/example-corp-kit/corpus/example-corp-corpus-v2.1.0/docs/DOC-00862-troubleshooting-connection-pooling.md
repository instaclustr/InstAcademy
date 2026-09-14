---
source_id: "DOC-00862"
title: "Troubleshooting connection pooling"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > Troubleshooting connection pooling"
product_area: "connectors"
product_version: "4.9"
acl: "standard"
updated_at: "2025-01-17"
related_error_codes: ["ERR-2231", "ERR-2288"]
---

# Troubleshooting connection pooling

Connection Pooling lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Audit events for connection pooling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

By default, connection pooling is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
