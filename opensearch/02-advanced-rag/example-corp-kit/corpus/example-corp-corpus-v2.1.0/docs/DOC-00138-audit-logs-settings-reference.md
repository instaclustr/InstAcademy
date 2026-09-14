---
source_id: "DOC-00138"
title: "Audit Logs settings reference"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > Audit Logs settings reference"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2025-01-29"
related_error_codes: ["ERR-7719"]
---

# Audit Logs settings reference

Audit Logs is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

By default, audit logs is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
