---
source_id: "DOC-00610"
title: "Usage Analytics settings reference"
doc_type: "product-docs"
section_path: "Administration > Usage Analytics > Usage Analytics settings reference"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2026-06-01"
related_error_codes: ["ERR-7733"]
---

# Usage Analytics settings reference

This page explains how usage analytics works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: usage analytics performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable usage analytics, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, usage analytics is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, usage analytics inherits group membership from your identity provider on each login.

Audit events for usage analytics are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
