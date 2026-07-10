---
source_id: "DOC-00037"
title: "Rate Limits overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > Rate Limits overview"
product_area: "api"
product_version: "5.0"
acl: "public"
updated_at: "2025-11-10"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# Rate Limits overview

Rate Limits lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, rate limits is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, rate limits inherits group membership from your identity provider on each login.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
