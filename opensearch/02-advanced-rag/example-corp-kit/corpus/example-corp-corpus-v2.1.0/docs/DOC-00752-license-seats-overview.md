---
source_id: "DOC-00752"
title: "License Seats overview"
doc_type: "product-docs"
section_path: "Administration > License Seats > License Seats overview"
product_area: "admin"
product_version: "4.9"
acl: "standard"
updated_at: "2024-11-02"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# License Seats overview

License Seats lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

When license seats is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, license seats is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
