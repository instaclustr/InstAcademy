---
source_id: "DOC-00421"
title: "Troubleshooting workspace permissions"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > Troubleshooting workspace permissions"
product_area: "admin"
product_version: "4.9"
acl: "enterprise"
updated_at: "2024-05-20"
related_error_codes: ["ERR-7733"]
---

# Troubleshooting workspace permissions

Workspace Permissions is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, workspace permissions inherits group membership from your identity provider on each login.

Audit events for workspace permissions are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, workspace permissions is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
