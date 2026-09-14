---
source_id: "DOC-00559"
title: "How to configure SAML SSO"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > How to configure SAML SSO"
product_area: "admin"
product_version: "4.9"
acl: "public"
updated_at: "2025-03-06"
related_error_codes: ["ERR-7733"]
---

# How to configure SAML SSO

Saml Sso lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

By default, SAML SSO is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
