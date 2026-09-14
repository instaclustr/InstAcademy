---
source_id: "DOC-00705"
title: "How license seats works"
doc_type: "product-docs"
section_path: "Administration > License Seats > How license seats works"
product_area: "admin"
product_version: "5.1"
acl: "professional"
updated_at: "2025-05-31"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# How license seats works

License Seats is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, license seats is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When license seats is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
