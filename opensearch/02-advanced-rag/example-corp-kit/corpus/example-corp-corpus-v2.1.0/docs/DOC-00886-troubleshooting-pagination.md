---
source_id: "DOC-00886"
title: "Troubleshooting pagination"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > Troubleshooting pagination"
product_area: "api"
product_version: "5.0"
acl: "public"
updated_at: "2024-09-09"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# Troubleshooting pagination

Pagination lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, pagination inherits group membership from your identity provider on each login.

Audit events for pagination are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, pagination is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When pagination is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
