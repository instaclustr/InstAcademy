---
source_id: "DOC-00227"
title: "How webhook signatures works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > How webhook signatures works"
product_area: "api"
product_version: "5.0"
acl: "standard"
updated_at: "2025-03-07"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# How webhook signatures works

Webhook Signatures lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, webhook signatures is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
