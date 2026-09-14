---
source_id: "DOC-00892"
title: "Troubleshooting usage analytics"
doc_type: "product-docs"
section_path: "Administration > Usage Analytics > Troubleshooting usage analytics"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2025-07-01"
related_error_codes: ["ERR-7733"]
---

# Troubleshooting usage analytics

Usage Analytics lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Audit events for usage analytics are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, usage analytics inherits group membership from your identity provider on each login.

Performance tip: usage analytics performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When usage analytics is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, usage analytics is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
