---
source_id: "DOC-00443"
title: "How schema discovery works"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > How schema discovery works"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2025-05-06"
related_error_codes: ["ERR-2209", "ERR-2288"]
---

# How schema discovery works

This page explains how schema discovery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, schema discovery is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When schema discovery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

Performance tip: schema discovery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
