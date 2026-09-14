---
source_id: "DOC-00560"
title: "How to configure SCIM provisioning"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > How to configure SCIM provisioning"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2024-03-12"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# How to configure SCIM provisioning

Scim Provisioning is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, SCIM provisioning is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
