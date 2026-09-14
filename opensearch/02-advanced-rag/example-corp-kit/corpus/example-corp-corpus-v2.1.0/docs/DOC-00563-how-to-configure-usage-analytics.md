---
source_id: "DOC-00563"
title: "How to configure usage analytics"
doc_type: "product-docs"
section_path: "Administration > Usage Analytics > How to configure usage analytics"
product_area: "admin"
product_version: "4.9"
acl: "standard"
updated_at: "2024-10-07"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# How to configure usage analytics

Usage Analytics lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

When usage analytics is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, usage analytics is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable usage analytics, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: usage analytics performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for usage analytics are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
