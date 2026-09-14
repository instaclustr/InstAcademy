---
source_id: "DOC-00609"
title: "Workspace Permissions settings reference"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > Workspace Permissions settings reference"
product_area: "admin"
product_version: "4.9"
acl: "public"
updated_at: "2026-02-07"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# Workspace Permissions settings reference

Workspace Permissions lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

Audit events for workspace permissions are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, workspace permissions is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When workspace permissions is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, workspace permissions inherits group membership from your identity provider on each login.

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
