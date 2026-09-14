---
source_id: "DOC-00091"
title: "How to configure audit logs"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > How to configure audit logs"
product_area: "admin"
product_version: "4.9"
acl: "standard"
updated_at: "2025-03-17"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# How to configure audit logs

This page explains how audit logs works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
