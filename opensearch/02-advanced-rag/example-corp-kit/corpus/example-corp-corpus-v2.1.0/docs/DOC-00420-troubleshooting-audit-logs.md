---
source_id: "DOC-00420"
title: "Troubleshooting audit logs"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > Troubleshooting audit logs"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2024-10-17"
related_error_codes: ["ERR-7719"]
---

# Troubleshooting audit logs

Audit Logs is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, audit logs is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
