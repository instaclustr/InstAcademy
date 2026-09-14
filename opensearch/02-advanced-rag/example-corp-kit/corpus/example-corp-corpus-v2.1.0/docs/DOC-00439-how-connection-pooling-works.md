---
source_id: "DOC-00439"
title: "How connection pooling works"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > How connection pooling works"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2024-12-10"
related_error_codes: ["ERR-2288"]
---

# How connection pooling works

Connection Pooling lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

Audit events for connection pooling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, connection pooling is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
