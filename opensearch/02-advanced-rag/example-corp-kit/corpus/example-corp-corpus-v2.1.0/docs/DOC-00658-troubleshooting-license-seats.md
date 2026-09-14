---
source_id: "DOC-00658"
title: "Troubleshooting license seats"
doc_type: "product-docs"
section_path: "Administration > License Seats > Troubleshooting license seats"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2024-10-21"
related_error_codes: ["ERR-7733"]
---

# Troubleshooting license seats

License Seats lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, license seats is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

When license seats is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
