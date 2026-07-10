---
source_id: "DOC-00890"
title: "Troubleshooting audit logs"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > Troubleshooting audit logs"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2025-02-13"
related_error_codes: ["ERR-7733"]
---

# Troubleshooting audit logs

This page explains how audit logs works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
