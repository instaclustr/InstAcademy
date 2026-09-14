---
source_id: "DOC-00373"
title: "Audit Logs settings reference"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > Audit Logs settings reference"
product_area: "admin"
product_version: "5.1"
acl: "professional"
updated_at: "2024-07-10"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# Audit Logs settings reference

Audit Logs lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

By default, audit logs is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
