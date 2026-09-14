---
source_id: "DOC-00376"
title: "License Seats settings reference"
doc_type: "product-docs"
section_path: "Administration > License Seats > License Seats settings reference"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2024-03-11"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# License Seats settings reference

License Seats is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

By default, license seats is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
