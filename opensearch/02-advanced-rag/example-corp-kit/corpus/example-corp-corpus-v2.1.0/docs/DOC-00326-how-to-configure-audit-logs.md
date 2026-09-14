---
source_id: "DOC-00326"
title: "How to configure audit logs"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > How to configure audit logs"
product_area: "admin"
product_version: "5.0"
acl: "professional"
updated_at: "2024-03-24"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# How to configure audit logs

Audit Logs lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, audit logs is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
