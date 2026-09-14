---
source_id: "DOC-00535"
title: "How to configure SSH tunneling"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > How to configure SSH tunneling"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2026-02-23"
related_error_codes: ["ERR-2231"]
---

# How to configure SSH tunneling

Ssh Tunneling is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

By default, SSH tunneling is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for SSH tunneling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
