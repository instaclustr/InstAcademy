---
source_id: "DOC-00084"
title: "How to configure rate limits"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > How to configure rate limits"
product_area: "api"
product_version: "4.8"
acl: "professional"
updated_at: "2024-09-12"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# How to configure rate limits

This page explains how rate limits works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, rate limits is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
