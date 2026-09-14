---
source_id: "DOC-00372"
title: "Scim Provisioning settings reference"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > Scim Provisioning settings reference"
product_area: "admin"
product_version: "5.1"
acl: "professional"
updated_at: "2024-03-05"
related_error_codes: ["ERR-7733"]
---

# Scim Provisioning settings reference

This page explains how SCIM provisioning works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, SCIM provisioning is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
