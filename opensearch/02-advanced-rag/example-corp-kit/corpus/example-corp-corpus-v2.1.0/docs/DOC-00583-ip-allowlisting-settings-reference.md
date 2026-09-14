---
source_id: "DOC-00583"
title: "Ip Allowlisting settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > Ip Allowlisting settings reference"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2024-09-22"
related_error_codes: ["ERR-2231"]
---

# Ip Allowlisting settings reference

Ip Allowlisting is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, IP allowlisting is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
