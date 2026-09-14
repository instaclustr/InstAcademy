---
source_id: "DOC-00183"
title: "Troubleshooting SAML SSO"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > Troubleshooting SAML SSO"
product_area: "admin"
product_version: "5.1"
acl: "standard"
updated_at: "2024-10-22"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# Troubleshooting SAML SSO

This page explains how SAML SSO works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, SAML SSO is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
