---
source_id: "DOC-00747"
title: "Saml Sso overview"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > Saml Sso overview"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2025-12-09"
related_error_codes: ["ERR-7719"]
---

# Saml Sso overview

Saml Sso lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

By default, SAML SSO is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
