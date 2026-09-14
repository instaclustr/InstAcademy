---
source_id: "DOC-00795"
title: "How to configure SCIM provisioning"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > How to configure SCIM provisioning"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2024-06-02"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# How to configure SCIM provisioning

Scim Provisioning is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, SCIM provisioning is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
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
