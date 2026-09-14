---
source_id: "DOC-00137"
title: "Scim Provisioning settings reference"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > Scim Provisioning settings reference"
product_area: "admin"
product_version: "4.8"
acl: "standard"
updated_at: "2025-11-04"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# Scim Provisioning settings reference

This page explains how SCIM provisioning works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, SCIM provisioning is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
