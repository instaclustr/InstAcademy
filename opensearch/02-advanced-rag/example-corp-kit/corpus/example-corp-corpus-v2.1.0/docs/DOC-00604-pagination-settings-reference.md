---
source_id: "DOC-00604"
title: "Pagination settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > Pagination settings reference"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2024-03-15"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# Pagination settings reference

This page explains how pagination works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, pagination inherits group membership from your identity provider on each login.

By default, pagination is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When pagination is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: pagination performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
