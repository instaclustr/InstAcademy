---
source_id: "DOC-00042"
title: "Saml Sso overview"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > Saml Sso overview"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2024-06-08"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# Saml Sso overview

Saml Sso is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

By default, SAML SSO is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
