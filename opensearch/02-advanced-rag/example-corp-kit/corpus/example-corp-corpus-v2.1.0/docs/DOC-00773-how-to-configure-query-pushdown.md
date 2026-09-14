---
source_id: "DOC-00773"
title: "How to configure query pushdown"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > How to configure query pushdown"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2025-02-05"
related_error_codes: ["ERR-2231"]
---

# How to configure query pushdown

Query Pushdown is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, query pushdown is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable query pushdown, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for query pushdown are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When query pushdown is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
