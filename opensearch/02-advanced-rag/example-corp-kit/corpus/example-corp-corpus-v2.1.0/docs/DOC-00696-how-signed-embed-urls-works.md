---
source_id: "DOC-00696"
title: "How signed embed URLs works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Signed Embed Urls > How signed embed URLs works"
product_area: "api"
product_version: "4.9"
acl: "enterprise"
updated_at: "2024-10-31"
related_error_codes: ["ERR-6640"]
---

# How signed embed URLs works

Signed Embed Urls lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Performance tip: signed embed URLs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable signed embed URLs, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, signed embed URLs is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, signed embed URLs inherits group membership from your identity provider on each login.

When signed embed URLs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
