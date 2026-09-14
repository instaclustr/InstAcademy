---
source_id: "DOC-00512"
title: "Saml Sso overview"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > Saml Sso overview"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2026-06-22"
related_error_codes: ["ERR-7719"]
---

# Saml Sso overview

Saml Sso is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: SAML SSO performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, SAML SSO is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
