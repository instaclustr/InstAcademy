---
source_id: "DOC-00631"
title: "Troubleshooting schema discovery"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > Troubleshooting schema discovery"
product_area: "connectors"
product_version: "5.1"
acl: "professional"
updated_at: "2025-02-06"
related_error_codes: ["ERR-2288"]
---

# Troubleshooting schema discovery

This page explains how schema discovery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, schema discovery is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable schema discovery, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: schema discovery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When schema discovery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
