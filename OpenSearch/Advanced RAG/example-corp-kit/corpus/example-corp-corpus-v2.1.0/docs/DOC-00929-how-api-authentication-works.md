---
source_id: "DOC-00929"
title: "How API authentication works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > How API authentication works"
product_area: "api"
product_version: "4.8"
acl: "professional"
updated_at: "2024-04-04"
related_error_codes: ["ERR-6640"]
---

# How API authentication works

Api Authentication lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

Performance tip: API authentication performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, API authentication inherits group membership from your identity provider on each login.

To enable API authentication, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, API authentication is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When API authentication is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
