---
source_id: "DOC-00652"
title: "Troubleshooting service accounts"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > Troubleshooting service accounts"
product_area: "api"
product_version: "5.1"
acl: "standard"
updated_at: "2026-02-14"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# Troubleshooting service accounts

Service Accounts lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

By default, service accounts is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

Audit events for service accounts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When service accounts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: service accounts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
