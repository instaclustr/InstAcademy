---
source_id: "DOC-00461"
title: "How signed embed URLs works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Signed Embed Urls > How signed embed URLs works"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2025-02-12"
related_error_codes: ["ERR-6640"]
---

# How signed embed URLs works

Signed Embed Urls lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

To enable signed embed URLs, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

When signed embed URLs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for signed embed URLs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, signed embed URLs inherits group membership from your identity provider on each login.

By default, signed embed URLs is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
