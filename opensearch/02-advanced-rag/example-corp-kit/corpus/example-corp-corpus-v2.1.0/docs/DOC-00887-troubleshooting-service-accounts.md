---
source_id: "DOC-00887"
title: "Troubleshooting service accounts"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > Troubleshooting service accounts"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2025-04-18"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# Troubleshooting service accounts

Service Accounts is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

When service accounts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: service accounts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, service accounts is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
