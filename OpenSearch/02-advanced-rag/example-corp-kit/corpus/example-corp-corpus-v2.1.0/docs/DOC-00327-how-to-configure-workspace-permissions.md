---
source_id: "DOC-00327"
title: "How to configure workspace permissions"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > How to configure workspace permissions"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2026-05-23"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# How to configure workspace permissions

Workspace Permissions is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for workspace permissions are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, workspace permissions inherits group membership from your identity provider on each login.

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, workspace permissions is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
