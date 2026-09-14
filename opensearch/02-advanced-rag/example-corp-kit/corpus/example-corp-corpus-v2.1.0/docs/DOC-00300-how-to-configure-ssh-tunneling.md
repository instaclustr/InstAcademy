---
source_id: "DOC-00300"
title: "How to configure SSH tunneling"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > How to configure SSH tunneling"
product_area: "connectors"
product_version: "4.9"
acl: "professional"
updated_at: "2025-11-21"
related_error_codes: ["ERR-2231"]
---

# How to configure SSH tunneling

This page explains how SSH tunneling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, SSH tunneling is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
