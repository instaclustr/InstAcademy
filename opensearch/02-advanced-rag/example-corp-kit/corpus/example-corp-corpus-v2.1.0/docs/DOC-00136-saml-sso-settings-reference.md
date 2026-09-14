---
source_id: "DOC-00136"
title: "Saml Sso settings reference"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > Saml Sso settings reference"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2024-04-29"
related_error_codes: ["ERR-7733"]
---

# Saml Sso settings reference

This page explains how SAML SSO works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: SAML SSO performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, SAML SSO is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
