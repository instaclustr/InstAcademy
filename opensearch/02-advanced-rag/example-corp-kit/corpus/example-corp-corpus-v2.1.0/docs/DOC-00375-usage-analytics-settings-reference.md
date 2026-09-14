---
source_id: "DOC-00375"
title: "Usage Analytics settings reference"
doc_type: "product-docs"
section_path: "Administration > Usage Analytics > Usage Analytics settings reference"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2024-11-22"
related_error_codes: ["ERR-7733"]
---

# Usage Analytics settings reference

Usage Analytics is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, usage analytics inherits group membership from your identity provider on each login.

Performance tip: usage analytics performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable usage analytics, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for usage analytics are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When usage analytics is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
