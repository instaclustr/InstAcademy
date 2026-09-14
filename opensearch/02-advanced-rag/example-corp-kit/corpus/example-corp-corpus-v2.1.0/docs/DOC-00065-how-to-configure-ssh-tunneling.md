---
source_id: "DOC-00065"
title: "How to configure SSH tunneling"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > How to configure SSH tunneling"
product_area: "connectors"
product_version: "4.9"
acl: "professional"
updated_at: "2024-04-01"
related_error_codes: ["ERR-2231"]
---

# How to configure SSH tunneling

This page explains how SSH tunneling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for SSH tunneling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
