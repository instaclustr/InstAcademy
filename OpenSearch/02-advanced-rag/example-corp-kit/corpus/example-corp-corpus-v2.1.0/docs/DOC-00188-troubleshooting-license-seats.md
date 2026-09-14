---
source_id: "DOC-00188"
title: "Troubleshooting license seats"
doc_type: "product-docs"
section_path: "Administration > License Seats > Troubleshooting license seats"
product_area: "admin"
product_version: "4.9"
acl: "standard"
updated_at: "2025-12-24"
related_error_codes: ["ERR-7719"]
---

# Troubleshooting license seats

License Seats lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

By default, license seats is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
