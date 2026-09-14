---
source_id: "DOC-00982"
title: "Saml Sso overview"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > Saml Sso overview"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2025-02-15"
related_error_codes: ["ERR-7733"]
---

# Saml Sso overview

Saml Sso lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

By default, SAML SSO is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
