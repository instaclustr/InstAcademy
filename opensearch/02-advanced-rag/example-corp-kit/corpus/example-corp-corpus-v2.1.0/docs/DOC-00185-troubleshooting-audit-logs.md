---
source_id: "DOC-00185"
title: "Troubleshooting audit logs"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > Troubleshooting audit logs"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2024-07-23"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# Troubleshooting audit logs

Audit Logs lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
