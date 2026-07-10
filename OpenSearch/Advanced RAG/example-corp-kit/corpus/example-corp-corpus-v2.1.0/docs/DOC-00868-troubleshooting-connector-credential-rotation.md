---
source_id: "DOC-00868"
title: "Troubleshooting connector credential rotation"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > Troubleshooting connector credential rotation"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2024-04-18"
related_error_codes: ["ERR-2288"]
---

# Troubleshooting connector credential rotation

Connector Credential Rotation is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: connector credential rotation performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, connector credential rotation is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When connector credential rotation is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
