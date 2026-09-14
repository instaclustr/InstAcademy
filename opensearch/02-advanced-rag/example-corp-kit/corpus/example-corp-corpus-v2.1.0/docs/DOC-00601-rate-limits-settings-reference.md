---
source_id: "DOC-00601"
title: "Rate Limits settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > Rate Limits settings reference"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2024-05-24"
related_error_codes: ["ERR-6601"]
---

# Rate Limits settings reference

This page explains how rate limits works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, rate limits is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, rate limits inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
