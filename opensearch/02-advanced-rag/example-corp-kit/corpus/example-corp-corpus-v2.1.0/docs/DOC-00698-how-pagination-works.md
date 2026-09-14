---
source_id: "DOC-00698"
title: "How pagination works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > How pagination works"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2025-11-14"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# How pagination works

Pagination is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: pagination performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, pagination is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, pagination inherits group membership from your identity provider on each login.

When pagination is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
