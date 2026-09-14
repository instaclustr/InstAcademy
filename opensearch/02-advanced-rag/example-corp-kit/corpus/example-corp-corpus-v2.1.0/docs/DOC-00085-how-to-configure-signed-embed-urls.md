---
source_id: "DOC-00085"
title: "How to configure signed embed URLs"
doc_type: "product-docs"
section_path: "REST API & Embedding > Signed Embed Urls > How to configure signed embed URLs"
product_area: "api"
product_version: "4.9"
acl: "professional"
updated_at: "2025-07-17"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# How to configure signed embed URLs

Signed Embed Urls lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, signed embed URLs inherits group membership from your identity provider on each login.

When signed embed URLs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for signed embed URLs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, signed embed URLs is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable signed embed URLs, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
