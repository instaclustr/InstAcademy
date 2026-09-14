---
source_id: "DOC-00888"
title: "Troubleshooting SAML SSO"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > Troubleshooting SAML SSO"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2026-01-31"
related_error_codes: ["ERR-7733"]
---

# Troubleshooting SAML SSO

This page explains how SAML SSO works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, SAML SSO is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
