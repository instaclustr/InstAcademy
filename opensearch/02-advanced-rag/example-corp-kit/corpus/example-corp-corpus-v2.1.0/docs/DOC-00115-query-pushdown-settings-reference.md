---
source_id: "DOC-00115"
title: "Query Pushdown settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > Query Pushdown settings reference"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2024-10-21"
related_error_codes: ["ERR-2231"]
---

# Query Pushdown settings reference

This page explains how query pushdown works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, query pushdown is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When query pushdown is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

Audit events for query pushdown are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
