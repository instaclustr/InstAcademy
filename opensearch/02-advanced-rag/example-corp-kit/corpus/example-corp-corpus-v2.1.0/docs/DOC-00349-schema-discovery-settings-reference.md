---
source_id: "DOC-00349"
title: "Schema Discovery settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > Schema Discovery settings reference"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2024-09-30"
related_error_codes: ["ERR-2288", "ERR-2231"]
---

# Schema Discovery settings reference

This page explains how schema discovery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, schema discovery is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

To enable schema discovery, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When schema discovery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
