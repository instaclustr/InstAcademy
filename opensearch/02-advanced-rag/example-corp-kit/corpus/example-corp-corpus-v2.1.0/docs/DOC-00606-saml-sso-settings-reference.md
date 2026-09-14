---
source_id: "DOC-00606"
title: "Saml Sso settings reference"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > Saml Sso settings reference"
product_area: "admin"
product_version: "4.9"
acl: "public"
updated_at: "2025-12-06"
related_error_codes: ["ERR-7719"]
---

# Saml Sso settings reference

Saml Sso lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, SAML SSO is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: SAML SSO performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
