---
source_id: "DOC-00465"
title: "How SAML SSO works"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > How SAML SSO works"
product_area: "admin"
product_version: "4.8"
acl: "standard"
updated_at: "2025-06-24"
related_error_codes: ["ERR-7719"]
---

# How SAML SSO works

This page explains how SAML SSO works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, SAML SSO is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
