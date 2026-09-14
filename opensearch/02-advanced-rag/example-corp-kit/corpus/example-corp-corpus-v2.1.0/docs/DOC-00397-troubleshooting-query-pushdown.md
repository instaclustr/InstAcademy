---
source_id: "DOC-00397"
title: "Troubleshooting query pushdown"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > Troubleshooting query pushdown"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2025-03-19"
related_error_codes: ["ERR-2288", "ERR-2209"]
---

# Troubleshooting query pushdown

Query Pushdown is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

Audit events for query pushdown are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable query pushdown, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, query pushdown is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
