---
source_id: "DOC-00843"
title: "Audit Logs settings reference"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > Audit Logs settings reference"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2024-09-03"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# Audit Logs settings reference

Audit Logs lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, audit logs is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
