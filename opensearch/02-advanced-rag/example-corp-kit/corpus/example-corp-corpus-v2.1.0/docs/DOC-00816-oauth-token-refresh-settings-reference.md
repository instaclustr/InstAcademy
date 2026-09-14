---
source_id: "DOC-00816"
title: "Oauth Token Refresh settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > Oauth Token Refresh settings reference"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2026-01-16"
related_error_codes: ["ERR-2209"]
---

# Oauth Token Refresh settings reference

This page explains how OAuth token refresh works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable OAuth token refresh, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, OAuth token refresh is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
