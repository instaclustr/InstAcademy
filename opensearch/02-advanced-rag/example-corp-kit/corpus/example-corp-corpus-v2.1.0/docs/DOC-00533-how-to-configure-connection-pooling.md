---
source_id: "DOC-00533"
title: "How to configure connection pooling"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > How to configure connection pooling"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2025-06-07"
related_error_codes: ["ERR-2288", "ERR-2231"]
---

# How to configure connection pooling

Connection Pooling is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for connection pooling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

By default, connection pooling is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
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
