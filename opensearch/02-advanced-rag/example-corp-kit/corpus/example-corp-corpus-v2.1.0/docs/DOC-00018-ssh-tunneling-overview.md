---
source_id: "DOC-00018"
title: "Ssh Tunneling overview"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > Ssh Tunneling overview"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2026-04-14"
related_error_codes: ["ERR-2288", "ERR-2209"]
---

# Ssh Tunneling overview

Ssh Tunneling is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for SSH tunneling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, SSH tunneling is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
