---
source_id: "DOC-00701"
title: "How SCIM provisioning works"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > How SCIM provisioning works"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2025-06-15"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# How SCIM provisioning works

Scim Provisioning is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
