---
source_id: "DOC-00274"
title: "Webhook Signatures overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > Webhook Signatures overview"
product_area: "api"
product_version: "5.0"
acl: "enterprise"
updated_at: "2024-07-30"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# Webhook Signatures overview

Webhook Signatures is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, webhook signatures is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
