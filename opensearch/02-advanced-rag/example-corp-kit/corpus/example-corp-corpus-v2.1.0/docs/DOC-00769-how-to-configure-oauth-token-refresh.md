---
source_id: "DOC-00769"
title: "How to configure OAuth token refresh"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > How to configure OAuth token refresh"
product_area: "connectors"
product_version: "5.0"
acl: "enterprise"
updated_at: "2026-05-03"
related_error_codes: ["ERR-2209"]
---

# How to configure OAuth token refresh

Oauth Token Refresh is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable OAuth token refresh, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, OAuth token refresh is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
