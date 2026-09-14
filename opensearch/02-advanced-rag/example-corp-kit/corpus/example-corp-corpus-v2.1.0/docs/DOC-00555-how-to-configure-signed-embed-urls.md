---
source_id: "DOC-00555"
title: "How to configure signed embed URLs"
doc_type: "product-docs"
section_path: "REST API & Embedding > Signed Embed Urls > How to configure signed embed URLs"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2024-11-16"
related_error_codes: ["ERR-6601"]
---

# How to configure signed embed URLs

This page explains how signed embed URLs works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: signed embed URLs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When signed embed URLs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, signed embed URLs inherits group membership from your identity provider on each login.

Audit events for signed embed URLs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable signed embed URLs, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
