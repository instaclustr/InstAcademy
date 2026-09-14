---
source_id: "DOC-00748"
title: "Scim Provisioning overview"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > Scim Provisioning overview"
product_area: "admin"
product_version: "5.1"
acl: "standard"
updated_at: "2025-02-09"
related_error_codes: ["ERR-7733"]
---

# Scim Provisioning overview

Scim Provisioning is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

By default, SCIM provisioning is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
