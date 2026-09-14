---
source_id: "DOC-00702"
title: "How audit logs works"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > How audit logs works"
product_area: "admin"
product_version: "4.9"
acl: "standard"
updated_at: "2025-05-29"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# How audit logs works

Audit Logs is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, audit logs is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
