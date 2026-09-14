---
source_id: "DOC-00088"
title: "How to configure service accounts"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > How to configure service accounts"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2026-02-19"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# How to configure service accounts

This page explains how service accounts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When service accounts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for service accounts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: service accounts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
