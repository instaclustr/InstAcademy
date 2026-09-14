---
source_id: "DOC-00648"
title: "Troubleshooting rate limits"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > Troubleshooting rate limits"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2024-02-18"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# Troubleshooting rate limits

Rate Limits is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, rate limits is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
