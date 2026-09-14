---
source_id: "DOC-00413"
title: "Troubleshooting rate limits"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > Troubleshooting rate limits"
product_area: "api"
product_version: "4.9"
acl: "professional"
updated_at: "2024-10-22"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# Troubleshooting rate limits

Rate Limits is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, rate limits inherits group membership from your identity provider on each login.

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, rate limits is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
