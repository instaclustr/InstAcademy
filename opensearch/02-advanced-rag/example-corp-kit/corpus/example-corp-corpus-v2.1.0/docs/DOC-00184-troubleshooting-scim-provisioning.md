---
source_id: "DOC-00184"
title: "Troubleshooting SCIM provisioning"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > Troubleshooting SCIM provisioning"
product_area: "admin"
product_version: "5.1"
acl: "professional"
updated_at: "2024-11-11"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# Troubleshooting SCIM provisioning

Scim Provisioning is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, SCIM provisioning is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
