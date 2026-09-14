---
source_id: "DOC-00514"
title: "Audit Logs overview"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > Audit Logs overview"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2025-09-06"
related_error_codes: ["ERR-7719"]
---

# Audit Logs overview

Audit Logs lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, audit logs is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
