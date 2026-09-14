---
source_id: "DOC-00346"
title: "Oauth Token Refresh settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > Oauth Token Refresh settings reference"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2024-02-29"
related_error_codes: ["ERR-2288", "ERR-2209"]
---

# Oauth Token Refresh settings reference

Oauth Token Refresh is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, OAuth token refresh inherits group membership from your identity provider on each login.

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, OAuth token refresh is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

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

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
