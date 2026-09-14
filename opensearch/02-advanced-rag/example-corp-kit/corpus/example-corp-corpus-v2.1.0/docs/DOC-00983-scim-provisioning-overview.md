---
source_id: "DOC-00983"
title: "Scim Provisioning overview"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > Scim Provisioning overview"
product_area: "admin"
product_version: "4.9"
acl: "enterprise"
updated_at: "2024-04-24"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# Scim Provisioning overview

Scim Provisioning lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

By default, SCIM provisioning is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
