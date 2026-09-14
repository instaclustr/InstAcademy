---
source_id: "DOC-00280"
title: "Workspace Permissions overview"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > Workspace Permissions overview"
product_area: "admin"
product_version: "4.9"
acl: "public"
updated_at: "2025-03-01"
related_error_codes: ["ERR-7719"]
---

# Workspace Permissions overview

Workspace Permissions lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When workspace permissions is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, workspace permissions inherits group membership from your identity provider on each login.

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, workspace permissions is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
