---
source_id: "DOC-00564"
title: "How to configure license seats"
doc_type: "product-docs"
section_path: "Administration > License Seats > How to configure license seats"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2024-09-28"
related_error_codes: ["ERR-7733"]
---

# How to configure license seats

License Seats is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, license seats is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
