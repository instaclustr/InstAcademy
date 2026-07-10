---
source_id: "DOC-00842"
title: "Scim Provisioning settings reference"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > Scim Provisioning settings reference"
product_area: "admin"
product_version: "4.9"
acl: "public"
updated_at: "2025-03-01"
related_error_codes: ["ERR-7733"]
---

# Scim Provisioning settings reference

Scim Provisioning lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

By default, SCIM provisioning is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
