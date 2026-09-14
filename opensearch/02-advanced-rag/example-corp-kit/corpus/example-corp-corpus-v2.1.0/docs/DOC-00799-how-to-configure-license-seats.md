---
source_id: "DOC-00799"
title: "How to configure license seats"
doc_type: "product-docs"
section_path: "Administration > License Seats > How to configure license seats"
product_area: "admin"
product_version: "4.9"
acl: "public"
updated_at: "2026-05-23"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# How to configure license seats

License Seats lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

By default, license seats is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When license seats is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
