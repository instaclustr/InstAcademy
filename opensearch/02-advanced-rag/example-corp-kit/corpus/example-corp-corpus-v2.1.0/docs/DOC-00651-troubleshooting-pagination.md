---
source_id: "DOC-00651"
title: "Troubleshooting pagination"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > Troubleshooting pagination"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2025-04-14"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# Troubleshooting pagination

Pagination lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

Performance tip: pagination performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, pagination inherits group membership from your identity provider on each login.

By default, pagination is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for pagination are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
