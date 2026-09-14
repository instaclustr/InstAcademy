---
source_id: "DOC-00351"
title: "Connector Credential Rotation settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > Connector Credential Rotation settings reference"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2026-01-11"
related_error_codes: ["ERR-2231", "ERR-2288"]
---

# Connector Credential Rotation settings reference

Connector Credential Rotation is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: connector credential rotation performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, connector credential rotation inherits group membership from your identity provider on each login.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, connector credential rotation is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
