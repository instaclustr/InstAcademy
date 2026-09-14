---
source_id: "DOC-00846"
title: "License Seats settings reference"
doc_type: "product-docs"
section_path: "Administration > License Seats > License Seats settings reference"
product_area: "admin"
product_version: "4.8"
acl: "professional"
updated_at: "2025-11-10"
related_error_codes: ["ERR-7719"]
---

# License Seats settings reference

License Seats is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, license seats is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
