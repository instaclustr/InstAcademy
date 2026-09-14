---
source_id: "DOC-00558"
title: "How to configure service accounts"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > How to configure service accounts"
product_area: "api"
product_version: "5.0"
acl: "public"
updated_at: "2024-10-09"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# How to configure service accounts

Service Accounts is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, service accounts is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

When service accounts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: service accounts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
