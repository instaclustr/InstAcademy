---
source_id: "DOC-00797"
title: "How to configure workspace permissions"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > How to configure workspace permissions"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2025-11-01"
related_error_codes: ["ERR-7733"]
---

# How to configure workspace permissions

Workspace Permissions is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When workspace permissions is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, workspace permissions inherits group membership from your identity provider on each login.

By default, workspace permissions is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
