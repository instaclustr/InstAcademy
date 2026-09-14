---
source_id: "DOC-00608"
title: "Audit Logs settings reference"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > Audit Logs settings reference"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2025-05-17"
related_error_codes: ["ERR-7719"]
---

# Audit Logs settings reference

This page explains how audit logs works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, audit logs inherits group membership from your identity provider on each login.

By default, audit logs is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
