---
source_id: "DOC-00700"
title: "How SAML SSO works"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > How SAML SSO works"
product_area: "admin"
product_version: "4.9"
acl: "public"
updated_at: "2024-08-19"
related_error_codes: ["ERR-7733"]
---

# How SAML SSO works

This page explains how SAML SSO works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

By default, SAML SSO is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
