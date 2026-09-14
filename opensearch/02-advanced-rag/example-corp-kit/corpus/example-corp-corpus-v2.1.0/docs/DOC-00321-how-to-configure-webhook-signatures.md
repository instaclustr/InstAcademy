---
source_id: "DOC-00321"
title: "How to configure webhook signatures"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > How to configure webhook signatures"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2026-03-04"
related_error_codes: ["ERR-6601"]
---

# How to configure webhook signatures

This page explains how webhook signatures works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, webhook signatures is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
