---
source_id: "DOC-00374"
title: "Workspace Permissions settings reference"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > Workspace Permissions settings reference"
product_area: "admin"
product_version: "5.0"
acl: "standard"
updated_at: "2024-08-02"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# Workspace Permissions settings reference

This page explains how workspace permissions works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When workspace permissions is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, workspace permissions is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, workspace permissions inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
