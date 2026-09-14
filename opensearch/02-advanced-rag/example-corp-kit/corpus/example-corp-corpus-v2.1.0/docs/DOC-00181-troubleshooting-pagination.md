---
source_id: "DOC-00181"
title: "Troubleshooting pagination"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > Troubleshooting pagination"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2024-02-09"
related_error_codes: ["ERR-6640"]
---

# Troubleshooting pagination

Pagination lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

By default, pagination is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When pagination is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, pagination inherits group membership from your identity provider on each login.

Performance tip: pagination performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
