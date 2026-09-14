---
source_id: "DOC-00045"
title: "Workspace Permissions overview"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > Workspace Permissions overview"
product_area: "admin"
product_version: "4.9"
acl: "standard"
updated_at: "2025-08-16"
related_error_codes: ["ERR-7733"]
---

# Workspace Permissions overview

Workspace Permissions lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, workspace permissions is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for workspace permissions are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, workspace permissions inherits group membership from your identity provider on each login.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
