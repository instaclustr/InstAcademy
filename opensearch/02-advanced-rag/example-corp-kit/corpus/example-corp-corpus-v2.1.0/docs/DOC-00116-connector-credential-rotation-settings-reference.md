---
source_id: "DOC-00116"
title: "Connector Credential Rotation settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > Connector Credential Rotation settings reference"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2024-03-01"
related_error_codes: ["ERR-2209"]
---

# Connector Credential Rotation settings reference

This page explains how connector credential rotation works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: connector credential rotation performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, connector credential rotation is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When connector credential rotation is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
