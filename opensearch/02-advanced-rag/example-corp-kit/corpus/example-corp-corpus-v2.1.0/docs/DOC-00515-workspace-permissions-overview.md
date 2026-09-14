---
source_id: "DOC-00515"
title: "Workspace Permissions overview"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > Workspace Permissions overview"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2026-02-12"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# Workspace Permissions overview

Workspace Permissions is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When workspace permissions is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, workspace permissions inherits group membership from your identity provider on each login.

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, workspace permissions is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for workspace permissions are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
