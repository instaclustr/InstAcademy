---
source_id: "DOC-00089"
title: "How to configure SAML SSO"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > How to configure SAML SSO"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2024-10-31"
related_error_codes: ["ERR-7733"]
---

# How to configure SAML SSO

Saml Sso is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: SAML SSO performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, SAML SSO is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
