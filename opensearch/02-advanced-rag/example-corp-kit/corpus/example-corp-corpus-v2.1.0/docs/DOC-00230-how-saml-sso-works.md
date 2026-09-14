---
source_id: "DOC-00230"
title: "How SAML SSO works"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > How SAML SSO works"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2025-02-10"
related_error_codes: ["ERR-7733"]
---

# How SAML SSO works

This page explains how SAML SSO works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: SAML SSO performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

By default, SAML SSO is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
