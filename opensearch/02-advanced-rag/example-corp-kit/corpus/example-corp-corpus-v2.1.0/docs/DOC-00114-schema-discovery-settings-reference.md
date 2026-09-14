---
source_id: "DOC-00114"
title: "Schema Discovery settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > Schema Discovery settings reference"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2025-04-25"
related_error_codes: ["ERR-2231"]
---

# Schema Discovery settings reference

This page explains how schema discovery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When schema discovery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

By default, schema discovery is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: schema discovery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
