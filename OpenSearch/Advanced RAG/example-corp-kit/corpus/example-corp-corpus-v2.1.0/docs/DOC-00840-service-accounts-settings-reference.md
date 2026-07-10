---
source_id: "DOC-00840"
title: "Service Accounts settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > Service Accounts settings reference"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2026-06-19"
related_error_codes: ["ERR-6601"]
---

# Service Accounts settings reference

Service Accounts is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: service accounts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, service accounts is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

Audit events for service accounts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
