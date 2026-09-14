---
source_id: "DOC-00742"
title: "Rate Limits overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > Rate Limits overview"
product_area: "api"
product_version: "5.0"
acl: "standard"
updated_at: "2024-12-29"
related_error_codes: ["ERR-6601"]
---

# Rate Limits overview

This page explains how rate limits works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, rate limits is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
