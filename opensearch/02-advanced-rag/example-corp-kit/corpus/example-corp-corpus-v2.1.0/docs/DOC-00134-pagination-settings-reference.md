---
source_id: "DOC-00134"
title: "Pagination settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > Pagination settings reference"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2024-05-02"
related_error_codes: ["ERR-6601"]
---

# Pagination settings reference

This page explains how pagination works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When pagination is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for pagination are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, pagination is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: pagination performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
