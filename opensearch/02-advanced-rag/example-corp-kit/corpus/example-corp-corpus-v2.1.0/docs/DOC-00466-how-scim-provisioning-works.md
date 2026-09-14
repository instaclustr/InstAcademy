---
source_id: "DOC-00466"
title: "How SCIM provisioning works"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > How SCIM provisioning works"
product_area: "admin"
product_version: "4.9"
acl: "public"
updated_at: "2025-06-09"
related_error_codes: ["ERR-7733"]
---

# How SCIM provisioning works

Scim Provisioning is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
