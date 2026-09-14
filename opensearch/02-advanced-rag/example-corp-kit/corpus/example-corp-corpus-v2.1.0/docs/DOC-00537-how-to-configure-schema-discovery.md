---
source_id: "DOC-00537"
title: "How to configure schema discovery"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > How to configure schema discovery"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2024-12-24"
related_error_codes: ["ERR-2231", "ERR-2288"]
---

# How to configure schema discovery

Schema Discovery is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When schema discovery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable schema discovery, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

By default, schema discovery is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
