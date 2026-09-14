---
source_id: "DOC-00838"
title: "Webhook Signatures settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > Webhook Signatures settings reference"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2025-03-13"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# Webhook Signatures settings reference

Webhook Signatures is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, webhook signatures is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
