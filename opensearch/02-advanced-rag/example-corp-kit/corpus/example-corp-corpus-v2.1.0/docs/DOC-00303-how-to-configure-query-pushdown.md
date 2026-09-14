---
source_id: "DOC-00303"
title: "How to configure query pushdown"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > How to configure query pushdown"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2026-06-14"
related_error_codes: ["ERR-2231"]
---

# How to configure query pushdown

Query Pushdown is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, query pushdown is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable query pushdown, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

When query pushdown is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
