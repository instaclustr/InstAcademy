---
source_id: "DOC-00112"
title: "Ssh Tunneling settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > Ssh Tunneling settings reference"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2026-01-24"
related_error_codes: ["ERR-2231"]
---

# Ssh Tunneling settings reference

Ssh Tunneling is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, SSH tunneling is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
