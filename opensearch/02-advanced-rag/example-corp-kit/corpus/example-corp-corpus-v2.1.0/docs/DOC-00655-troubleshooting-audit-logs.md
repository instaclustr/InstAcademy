---
source_id: "DOC-00655"
title: "Troubleshooting audit logs"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > Troubleshooting audit logs"
product_area: "admin"
product_version: "4.9"
acl: "public"
updated_at: "2025-08-20"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# Troubleshooting audit logs

This page explains how audit logs works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, audit logs is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
