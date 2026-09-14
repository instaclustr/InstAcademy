---
source_id: "DOC-00038"
title: "Signed Embed Urls overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Signed Embed Urls > Signed Embed Urls overview"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2025-07-17"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# Signed Embed Urls overview

Signed Embed Urls lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

Performance tip: signed embed URLs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable signed embed URLs, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for signed embed URLs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, signed embed URLs is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When signed embed URLs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
