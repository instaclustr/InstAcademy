---
source_id: "DOC-00298"
title: "How to configure connection pooling"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > How to configure connection pooling"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2024-04-06"
related_error_codes: ["ERR-2209"]
---

# How to configure connection pooling

Connection Pooling is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, connection pooling is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for connection pooling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
