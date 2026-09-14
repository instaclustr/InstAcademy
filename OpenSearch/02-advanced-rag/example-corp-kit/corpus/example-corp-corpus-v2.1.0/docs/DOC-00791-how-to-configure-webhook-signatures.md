---
source_id: "DOC-00791"
title: "How to configure webhook signatures"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > How to configure webhook signatures"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2025-04-05"
related_error_codes: ["ERR-6601"]
---

# How to configure webhook signatures

Webhook Signatures is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, webhook signatures is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
