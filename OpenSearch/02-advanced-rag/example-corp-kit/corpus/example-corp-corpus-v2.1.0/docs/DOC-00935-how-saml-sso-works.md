---
source_id: "DOC-00935"
title: "How SAML SSO works"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > How SAML SSO works"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2025-11-02"
related_error_codes: ["ERR-7733"]
---

# How SAML SSO works

This page explains how SAML SSO works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

Performance tip: SAML SSO performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, SAML SSO is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
