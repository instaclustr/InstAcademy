---
source_id: "DOC-00110"
title: "Connection Pooling settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > Connection Pooling settings reference"
product_area: "connectors"
product_version: "5.0"
acl: "professional"
updated_at: "2024-12-21"
related_error_codes: ["ERR-2209"]
---

# Connection Pooling settings reference

Connection Pooling is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, connection pooling is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for connection pooling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
