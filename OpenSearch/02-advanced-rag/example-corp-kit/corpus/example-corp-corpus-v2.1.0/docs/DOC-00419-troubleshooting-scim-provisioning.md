---
source_id: "DOC-00419"
title: "Troubleshooting SCIM provisioning"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > Troubleshooting SCIM provisioning"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2024-09-15"
related_error_codes: ["ERR-7733"]
---

# Troubleshooting SCIM provisioning

Scim Provisioning lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, SCIM provisioning is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
