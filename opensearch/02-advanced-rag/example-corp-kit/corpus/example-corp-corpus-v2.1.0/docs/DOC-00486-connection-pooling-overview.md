---
source_id: "DOC-00486"
title: "Connection Pooling overview"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > Connection Pooling overview"
product_area: "connectors"
product_version: "4.9"
acl: "enterprise"
updated_at: "2024-10-07"
related_error_codes: ["ERR-2288"]
---

# Connection Pooling overview

This page explains how connection pooling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for connection pooling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, connection pooling is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
