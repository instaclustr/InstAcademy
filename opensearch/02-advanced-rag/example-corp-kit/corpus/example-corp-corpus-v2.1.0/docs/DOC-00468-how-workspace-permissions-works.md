---
source_id: "DOC-00468"
title: "How workspace permissions works"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > How workspace permissions works"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2025-05-21"
related_error_codes: ["ERR-7719"]
---

# How workspace permissions works

Workspace Permissions is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for workspace permissions are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When workspace permissions is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, workspace permissions inherits group membership from your identity provider on each login.

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
