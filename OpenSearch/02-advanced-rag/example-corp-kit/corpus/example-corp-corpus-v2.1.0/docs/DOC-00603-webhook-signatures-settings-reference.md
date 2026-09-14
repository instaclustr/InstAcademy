---
source_id: "DOC-00603"
title: "Webhook Signatures settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > Webhook Signatures settings reference"
product_area: "api"
product_version: "5.0"
acl: "professional"
updated_at: "2026-06-14"
related_error_codes: ["ERR-6601"]
---

# Webhook Signatures settings reference

This page explains how webhook signatures works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, webhook signatures is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
