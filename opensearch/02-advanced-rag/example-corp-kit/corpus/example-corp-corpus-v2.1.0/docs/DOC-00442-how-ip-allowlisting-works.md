---
source_id: "DOC-00442"
title: "How IP allowlisting works"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > How IP allowlisting works"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2026-05-03"
related_error_codes: ["ERR-2288"]
---

# How IP allowlisting works

Ip Allowlisting lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, IP allowlisting is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
