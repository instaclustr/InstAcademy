---
source_id: "DOC-00841"
title: "Saml Sso settings reference"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > Saml Sso settings reference"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2026-02-10"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# Saml Sso settings reference

This page explains how SAML SSO works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, SAML SSO is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: SAML SSO performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
