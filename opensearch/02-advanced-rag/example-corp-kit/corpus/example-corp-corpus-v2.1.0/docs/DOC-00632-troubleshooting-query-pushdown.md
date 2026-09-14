---
source_id: "DOC-00632"
title: "Troubleshooting query pushdown"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > Troubleshooting query pushdown"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2025-04-15"
related_error_codes: ["ERR-2288"]
---

# Troubleshooting query pushdown

This page explains how query pushdown works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When query pushdown is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for query pushdown are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, query pushdown is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
