---
source_id: "DOC-00538"
title: "How to configure query pushdown"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > How to configure query pushdown"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2025-03-06"
related_error_codes: ["ERR-2288", "ERR-2209"]
---

# How to configure query pushdown

Query Pushdown is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, query pushdown is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When query pushdown is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable query pushdown, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
