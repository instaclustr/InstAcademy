---
source_id: "DOC-00938"
title: "How workspace permissions works"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > How workspace permissions works"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2026-02-18"
related_error_codes: ["ERR-7719"]
---

# How workspace permissions works

Workspace Permissions is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, workspace permissions inherits group membership from your identity provider on each login.

By default, workspace permissions is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When workspace permissions is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
