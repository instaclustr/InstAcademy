---
source_id: "DOC-00063"
title: "How to configure connection pooling"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > How to configure connection pooling"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2025-09-24"
related_error_codes: ["ERR-2209", "ERR-2288"]
---

# How to configure connection pooling

Connection Pooling is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, connection pooling is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
