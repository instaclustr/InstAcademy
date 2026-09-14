---
source_id: "DOC-00279"
title: "Audit Logs overview"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > Audit Logs overview"
product_area: "admin"
product_version: "4.8"
acl: "standard"
updated_at: "2025-06-17"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# Audit Logs overview

Audit Logs lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, audit logs is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
