---
source_id: "DOC-00893"
title: "Troubleshooting license seats"
doc_type: "product-docs"
section_path: "Administration > License Seats > Troubleshooting license seats"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2025-03-20"
related_error_codes: ["ERR-7719"]
---

# Troubleshooting license seats

License Seats is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When license seats is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
