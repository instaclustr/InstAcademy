---
source_id: "DOC-00697"
title: "How webhook signatures works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > How webhook signatures works"
product_area: "api"
product_version: "5.0"
acl: "public"
updated_at: "2024-02-07"
related_error_codes: ["ERR-6640"]
---

# How webhook signatures works

Webhook Signatures lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
