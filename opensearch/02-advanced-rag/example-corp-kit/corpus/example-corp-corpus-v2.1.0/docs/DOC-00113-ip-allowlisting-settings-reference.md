---
source_id: "DOC-00113"
title: "Ip Allowlisting settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > Ip Allowlisting settings reference"
product_area: "connectors"
product_version: "4.8"
acl: "professional"
updated_at: "2024-10-27"
related_error_codes: ["ERR-2231"]
---

# Ip Allowlisting settings reference

This page explains how IP allowlisting works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, IP allowlisting is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
