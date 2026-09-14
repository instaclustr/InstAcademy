---
source_id: "DOC-00679"
title: "How query pushdown works"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > How query pushdown works"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2026-05-18"
related_error_codes: ["ERR-2288"]
---

# How query pushdown works

Query Pushdown lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

By default, query pushdown is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for query pushdown are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When query pushdown is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
