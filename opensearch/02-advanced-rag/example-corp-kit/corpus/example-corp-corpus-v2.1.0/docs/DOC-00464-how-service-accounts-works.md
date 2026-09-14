---
source_id: "DOC-00464"
title: "How service accounts works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > How service accounts works"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2024-12-15"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# How service accounts works

Service Accounts is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: service accounts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for service accounts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, service accounts is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
