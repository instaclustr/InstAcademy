---
source_id: "DOC-00069"
title: "How to configure connector credential rotation"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > How to configure connector credential rotation"
product_area: "connectors"
product_version: "4.8"
acl: "enterprise"
updated_at: "2024-12-06"
related_error_codes: ["ERR-2209", "ERR-2288"]
---

# How to configure connector credential rotation

This page explains how connector credential rotation works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When connector credential rotation is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, connector credential rotation is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: connector credential rotation performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
