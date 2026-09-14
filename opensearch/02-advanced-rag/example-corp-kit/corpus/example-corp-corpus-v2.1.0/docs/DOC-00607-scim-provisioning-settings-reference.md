---
source_id: "DOC-00607"
title: "Scim Provisioning settings reference"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > Scim Provisioning settings reference"
product_area: "admin"
product_version: "4.9"
acl: "professional"
updated_at: "2025-01-28"
related_error_codes: ["ERR-7733"]
---

# Scim Provisioning settings reference

Scim Provisioning is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, SCIM provisioning is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
