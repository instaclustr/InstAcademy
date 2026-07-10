---
source_id: "DOC-00650"
title: "Troubleshooting webhook signatures"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > Troubleshooting webhook signatures"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2024-05-25"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# Troubleshooting webhook signatures

Webhook Signatures is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, webhook signatures is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
