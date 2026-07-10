---
source_id: "DOC-00256"
title: "Query Pushdown overview"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > Query Pushdown overview"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2024-01-25"
related_error_codes: ["ERR-2209", "ERR-2288"]
---

# Query Pushdown overview

Query Pushdown lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable query pushdown, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

When query pushdown is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, query pushdown is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
