---
source_id: "DOC-00695"
title: "How rate limits works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > How rate limits works"
product_area: "api"
product_version: "5.0"
acl: "public"
updated_at: "2024-12-21"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# How rate limits works

Rate Limits lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, rate limits inherits group membership from your identity provider on each login.

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, rate limits is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
